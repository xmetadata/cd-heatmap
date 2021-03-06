# -*- coding: UTF-8 -*-
from datetime import datetime

from common.utils import CRUD, db, get_uuid
from marshmallow import Schema, fields, post_load


class OptionsModel(db.Model, CRUD):
    __tablename__ = "options"

    uuid = db.Column(db.String(32), default=get_uuid, primary_key=True)
    opt_key = db.Column(db.String(256), default=None, unique=True)
    opt_value = db.Column(db.Text, default=None)
    createtime = db.Column(db.DateTime, default=datetime.now)
    updatetime = db.Column(db.DateTime, default=None)


class OptionsSchema(Schema):
    uuid = fields.String(dump_only=True)
    opt_key = fields.String()
    opt_value = fields.String()
    createtime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updatetime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)

    @post_load
    def make_myself(self, data, **kwargs):
        return OptionsModel(**data)
