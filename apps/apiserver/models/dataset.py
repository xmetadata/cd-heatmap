# -*- coding: UTF-8 -*-
from datetime import datetime

from common.utils import CRUD, db, get_uuid
from marshmallow import Schema, fields, post_load


class DatasetModel(db.Model, CRUD):
    __tablename__ = "dataset"

    uuid = db.Column(db.String(32), default=get_uuid, primary_key=True)
    title = db.Column(db.String(256), default=None, unique=True)
    catalog = db.Column(db.String(32), default=None)
    mode = db.Column(db.String(32), default=None)
    inc_area = db.Column(db.Boolean, default=False)
    tag = db.Column(db.String(32), default=None)
    headers = db.Column(db.Text, default=None)
    navigate = db.Column(db.Text, default=None)
    complete = db.Column(db.Boolean, default=False)
    createtime = db.Column(db.DateTime, default=datetime.now)
    updatetime = db.Column(db.DateTime, default=None)


class DatasetSchema(Schema):
    uuid = fields.String(dump_only=True)
    title = fields.String()
    catalog = fields.String()
    mode = fields.String()
    inc_area = fields.Boolean()
    tag = fields.String()
    headers = fields.String()
    navigate = fields.String()
    complete = fields.Boolean()
    createtime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updatetime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)

    @post_load
    def make_myself(self, data, **kwargs):
        return DatasetModel(**data)
