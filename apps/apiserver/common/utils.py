# -*- coding: UTF-8 -*-
from uuid import uuid1

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CRUD():
    def add(self, resource):
        db.session.add(resource)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        db.session.commit()


def pretty_response(code, data=None, message=None):
    default_message = {
        200: "请求成功",
        20001: "已创建",
        20002: "已修改",
        20003: "已删除",
        400: "客户端请求的语法错误，服务器无法理解",
        40001: "客户端数据验证失败",
        40002: "客户端提交重复数据",
        40003: "接口数据验证失败",
        401: "请求要求用户的身份认证",
        403: "服务器理解请求客户端的请求，但是拒绝执行此请求",
        404: "请求的资源(网页等)不存在",
        405: "客户端请求中的方法被禁止",
        500: "内部服务器错误",
        50001: "内部服务器数据库处理错误",
        50002: "内部服务器请求接口错误",
        50003: "内部服务器初始化配置错误",
    }
    http_code = int(code / 100) if code > 9999 else code
    if data is None:
        return {'message': message if message else default_message.get(code, ''), 'status_code': code}, http_code
    else:
        return data, http_code


def get_uuid():
    return uuid1().hex


def paginate_parse(paginate):
    return {
        'page': paginate.page,
        'per_page': paginate.per_page,
        'total': paginate.total,
        'pages': paginate.pages,
        'has_next': paginate.has_next,
        'has_prev': paginate.has_prev,
        'prev_num': paginate.prev_num,
        'next_num': paginate.next_num
    }
