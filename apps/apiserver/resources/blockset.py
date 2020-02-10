# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from common.utils import paginate_parse, pretty_response
from common.tasks import find_coordinates, find_centroid, calculate_area
from models.blockset import BlocksetModel, BlocksetSchema


class BlocksetList(Resource):
    @jwt_required()
    def get(self):
        """ Query all instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        paginate = BlocksetModel.query.filter(BlocksetModel.title.like(
            '%' + request.args.get('title', '') + '%')).paginate(page, per_page, max_per_page=100)
        data = paginate_parse(paginate)
        data['items'] = BlocksetSchema(many=True).dump(paginate.items)
        return pretty_response(200, data)

    @jwt_required()
    def post(self):
        """ Insert multi-instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        jsondata = request.get_json()
        if BlocksetModel.query.filter_by(title=jsondata.get('title', '')).first():
            return pretty_response(40002)
        try:
            coordinates = find_coordinates(jsondata.get('description', ''))
            if not coordinates:
                return pretty_response(40001)

            blockset_instance = BlocksetSchema().load(jsondata, unknown=EXCLUDE)
            blockset_instance.coordinates = json.dumps(coordinates)
            blockset_instance.centroid = json.dumps(find_centroid(coordinates))
            blockset_instance.area = calculate_area(coordinates)
            blockset_instance.add(blockset_instance)
            blockset_dump = BlocksetSchema().dump(blockset_instance)
            return pretty_response(200, blockset_dump)
        except ValidationError as e:
            current_app.logger.error(e.messages)
            return pretty_response(40003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)

    def put(self):
        """ Update multi-instances """
        blocksets = BlocksetModel.query.all()
        point_pool = []
        for blockset in blocksets:
            coordinates_temp = []
            coordinates = json.loads(blockset.coordinates)
            for coordinate in coordinates:
                aggregate_flag = False
                for point in point_pool:
                    if abs(coordinate.get('lng') - point.get('lng')) < 0.001 and abs(coordinate.get('lat') - point.get('lat')) < 0.001:
                        coordinates_temp.append(point)
                        aggregate_flag = True
                        break
                if not aggregate_flag:
                    coordinates_temp.append(coordinate)
                    point_pool.append(coordinate)
            blockset.coordinates = json.dumps(coordinates_temp)
            blockset.update()
        return pretty_response(200)

    def delete(self):
        """ Batch-delete instances """
        return pretty_response(405)


class Blockset(Resource):
    @jwt_required()
    def get(self, uuid):
        """ Query specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        blockset_instance = BlocksetModel.query.get_or_404(uuid)
        # print(json.loads(blockset_instance.centroid))
        blockset_dump = BlocksetSchema().dump(blockset_instance)
        blockset_dump['centroid'] = json.loads(blockset_instance.centroid)
        blockset_dump['coordinates'] = json.loads(blockset_instance.coordinates)
        print(blockset_dump)
        return pretty_response(200, blockset_dump)

    @jwt_required()
    def post(self, uuid):
        """ Update specific instance """
        return pretty_response(405)

    @jwt_required()
    def put(self, uuid):
        """ Update specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        blockset_instance = BlocksetModel.query.get_or_404(uuid)
        jsondata = request.get_json()
        try:
            coordinates = find_coordinates(jsondata.get('description', ''))
            if not coordinates:
                return pretty_response(40001)
            BlocksetSchema().load(jsondata, partial=("title", "description",), unknown=EXCLUDE)
            for key, val in jsondata.items():
                setattr(blockset_instance, key, val)
            blockset_instance.coordinates = json.dumps(coordinates)
            blockset_instance.centroid = json.dumps(find_centroid(coordinates))
            blockset_instance.area = calculate_area(coordinates)
            blockset_instance.updatetime = datetime.now()
            blockset_instance.update()
            blockset_dump = BlocksetSchema().dump(blockset_instance)
            return pretty_response(200, blockset_dump)
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
        blockset_instance = BlocksetModel.query.get_or_404(uuid)
        try:
            blockset_instance.delete(blockset_instance)
            return pretty_response(20003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            pretty_response(50001)
