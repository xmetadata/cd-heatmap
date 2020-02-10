# -*- coding: UTF-8 -*-
import threading
import json
import re
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from common.utils import paginate_parse, pretty_response
from common.tasks import analysis_dataset, analysis_dataset_block, fetch_collection, delete_collection
from models.dataset import DatasetModel, DatasetSchema
from models.blockset import BlocksetModel, BlocksetSchema


class DatasetList(Resource):
    @jwt_required()
    def get(self):
        """ Query all instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        title = request.args.get('title', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        paginate = DatasetModel.query.filter(DatasetModel.title.like('%' + title + '%')).paginate(
            page, per_page, max_per_page=100)
        data = paginate_parse(paginate)
        data['items'] = DatasetSchema(many=True).dump(paginate.items)
        return pretty_response(200, data)

    @jwt_required()
    def post(self):
        """ Insert multi-instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        jsondata = request.get_json()
        if DatasetModel.query.filter_by(title=jsondata['title']).first():
            return pretty_response(40002)
        headers = jsondata.get('header', [])
        catalog = jsondata.get('catalog', None)
        if '数值' not in headers \
                or (catalog == 'block' and '板块' not in headers) \
                or (catalog == 'point' and '标题' not in headers):
            return pretty_response(40001)
        try:
            dataset_instance = DatasetSchema().load(jsondata, unknown=EXCLUDE)
            dataset_instance.add(dataset_instance)

            blocksets = BlocksetModel.query.all()
            data = json.loads(
                re.sub(r'[\s+]', '', json.dumps(jsondata.get('data', []))))
            if catalog == 'block':
                # 导入板块数据
                t = threading.Thread(target=analysis_dataset_block, args=(
                    'T' + dataset_instance.uuid, data, blocksets, headers))
                t.start()
            else:
                # 导入集合数据
                t = threading.Thread(target=analysis_dataset, args=(
                    'T' + dataset_instance.uuid, data, blocksets, headers))
                t.start()

            dataset_dump = DatasetSchema().dump(dataset_instance)
            return pretty_response(200, dataset_dump)
        except ValidationError as e:
            current_app.logger.error(e.messages)
            return pretty_response(40003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)

    def put(self):
        """ Update multi-instances """
        return pretty_response(405)

    def delete(self):
        """ Batch-delete instances """
        return pretty_response(405)


class Dataset(Resource):
    @jwt_required()
    def get(self, uuid):
        """ Query specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        dataset_instance = DatasetModel.query.get_or_404(uuid)
        dataset_dump = DatasetSchema().dump(dataset_instance)
        result = fetch_collection('T' + dataset_instance.uuid, [])
        dataset_dump['data'] = result
        return pretty_response(200, dataset_dump)

    @jwt_required()
    def post(self, uuid):
        """ Update specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        dataset_instance = DatasetModel.query.get_or_404(uuid)

        jsondata = request.get_json()
        if not jsondata:
            return pretty_response(40001)

        catalog = jsondata.get('catalog', '')
        match = jsondata.get('match', {})

        pipeline = []
        aggregate_items = []
        aggregate_max = 0
        if catalog == 'block':
            pipeline = [{
                '$match': match
            }, {
                '$group': {'_id': "$板块", 'value': {dataset_instance.mode: '$数值'}}
            }]
            result = fetch_collection('T' + dataset_instance.uuid, pipeline)
            blockset_list = BlocksetModel.query.all()
            for blockset in blockset_list:
                temp = {
                    'title': blockset.title,
                    'area': blockset.area,
                    'centroid': json.loads(blockset.centroid),
                    'coordinates': json.loads(blockset.coordinates),
                    'org_value': 0,
                    'value': 0,
                }
                for item in result:
                    if blockset.title == item.get('_id', ''):
                        if not item.get('value', None):
                            break
                        item_value = item.get('value', 0)
                        temp['org_value'] = item_value
                        temp['value'] = round(
                            item_value / float(blockset.area), 4) if dataset_instance.inc_area else item_value
                        if temp['value'] > aggregate_max:
                            aggregate_max = temp['value']
                        break
                aggregate_items.append(temp)
        else:
            pipeline = [{
                '$match': match
            }]
            result = fetch_collection('T' + dataset_instance.uuid, pipeline)
            for item in result:
                aggregate_item = {
                    'title': item.get('标题', ''),
                    'address': item.get('地址', ''),
                    'lng': item.get('经度', ''),
                    'lat': item.get('纬度', ''),
                    'value': item.get('数值', 0),
                }
                if aggregate_item['value'] > aggregate_max:
                    aggregate_max = aggregate_item['value']
                aggregate_items.append(aggregate_item)
        return pretty_response(200, {'max': aggregate_max, 'items': aggregate_items})

    @jwt_required()
    def put(self, uuid):
        """ Update specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        dataset_instance = DatasetModel.query.get_or_404(uuid)
        try:
            jsondata = request.get_json()
            DatasetSchema().load(jsondata, unknown=EXCLUDE)
            for key, val in jsondata.items():
                setattr(dataset_instance, key, val)
            dataset_instance.updatetime = datetime.now()
            dataset_instance.update()
            dataset_dump = DatasetSchema().dump(dataset_instance)
            return pretty_response(200, dataset_dump)
        except ValidationError as e:
            current_app.logger.error(e.messages)
            return pretty_response(40003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)

    @jwt_required()
    def delete(self, uuid):
        """ Delete specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        dataset_instance = DatasetModel.query.get_or_404(uuid)
        delete_collection('T' + dataset_instance.uuid)
        try:
            dataset_instance.delete(dataset_instance)
            return pretty_response(20003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            pretty_response(50001)


class DatasetFree(Resource):
    def put(self, uuid):
        """ Update specific instance """
        dataset_instance = DatasetModel.query.get_or_404(uuid)
        try:
            jsondata = request.get_json()
            DatasetSchema().load(jsondata, unknown=EXCLUDE)
            for key, val in jsondata.items():
                setattr(dataset_instance, key, val)
            dataset_instance.updatetime = datetime.now()
            dataset_instance.update()
            dataset_dump = DatasetSchema().dump(dataset_instance)
            return pretty_response(200, dataset_dump)
        except ValidationError as e:
            current_app.logger.error(e.messages)
            return pretty_response(40003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)
