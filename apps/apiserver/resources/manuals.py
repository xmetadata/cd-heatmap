# -*- coding: UTF-8 -*-
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from common.utils import pretty_response
from models.manuals import ManualsModel, ManualsSchema


class ManualsList(Resource):
    @jwt_required()
    def get(self):
        """ Query all instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        if request.args.get('title'):
            manuals_list = ManualsModel.query.filter_by(
                title=request.args.get('title')).order_by("createtime").all()
        else:
            manuals_list = ManualsModel.query.order_by("createtime").all()
        manuals_dump = ManualsSchema(many=True).dump(manuals_list)
        return pretty_response(200, manuals_dump)

    @jwt_required()
    def post(self):
        """ Insert multi-instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        jsondata = request.get_json()
        if not jsondata or 'title' not in jsondata:
            return pretty_response(40001)
        if ManualsModel.query.filter_by(title=jsondata['title']).first():
            return pretty_response(40002)
        try:
            manuals_instance = ManualsSchema().load(jsondata)
            manuals_instance.add(manuals_instance)
            manuals_dump = ManualsSchema().dump(manuals_instance)
            return pretty_response(200, manuals_dump)
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


class Manuals(Resource):
    @jwt_required()
    def get(self, uuid):
        """ Query specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        manuals_instance = ManualsModel.query.get_or_404(uuid)
        manuals_dump = ManualsSchema().dump(manuals_instance)
        return pretty_response(200, manuals_dump)

    @jwt_required()
    def post(self, uuid):
        """ Update specific instance """
        return pretty_response(405)

    @jwt_required()
    def put(self, uuid):
        """ Update specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        manuals_instance = ManualsModel.query.get_or_404(uuid)
        try:
            jsondata = request.get_json()
            ManualsSchema().load(jsondata)
            for key, val in jsondata.items():
                setattr(manuals_instance, key, val)
            manuals_instance.updatetime = datetime.now()
            manuals_instance.update()
            manuals_dump = ManualsSchema().dump(manuals_instance)
            return pretty_response(200, manuals_dump)
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
        manuals_instance = ManualsModel.query.get_or_404(uuid)
        try:
            manuals_instance.delete(manuals_instance)
            return pretty_response(20003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            pretty_response(50001)
