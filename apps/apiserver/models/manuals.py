# -*- coding: UTF-8 -*-
from datetime import datetime

from common.utils import CRUD, db, get_uuid
from marshmallow import Schema, fields, post_load


class ManualsModel(db.Model, CRUD):
    __tablename__ = "manuals"

    uuid = db.Column(db.String(32), default=get_uuid, primary_key=True)
    title = db.Column(db.String(256), default=None, unique=True)
    content = db.Column(db.Text, default=None)
    createtime = db.Column(db.DateTime, default=datetime.now)
    updatetime = db.Column(db.DateTime, default=None)


class ManualsSchema(Schema):
    uuid = fields.String(dump_only=True)
    title = fields.String()
    content = fields.String()
    createtime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updatetime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)

    @post_load
    def make_myself(self, data, **kwargs):
        return ManualsModel(**data)
