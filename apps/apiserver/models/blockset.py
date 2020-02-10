# -*- coding: UTF-8 -*-
from datetime import datetime

from common.utils import CRUD, db, get_uuid
from marshmallow import Schema, fields, post_load


class BlocksetModel(db.Model, CRUD):
    __tablename__ = "blockset"

    uuid = db.Column(db.String(32), default=get_uuid, primary_key=True)
    title = db.Column(db.String(256), default=None, unique=True)
    description = db.Column(db.Text, default=None)
    coordinates = db.Column(db.Text, default=None)
    centroid = db.Column(db.Text, default=None)
    area = db.Column(db.String(32), default=None)
    createtime = db.Column(db.DateTime, default=datetime.now)
    updatetime = db.Column(db.DateTime, default=None)


class BlocksetSchema(Schema):
    uuid = fields.String(dump_only=True)
    title = fields.String()
    description = fields.String()
    coordinates = fields.String()
    centroid = fields.String()
    area = fields.String()
    createtime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updatetime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)

    @post_load
    def make_myself(self, data, **kwargs):
        return BlocksetModel(**data)
