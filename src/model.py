# -*- coding: utf-8 -*-
from conf import mongo_str, root_logger
from pymongo import MongoClient


class DBHandle:
    def __init__(self):
        self.client = MongoClient(mongo_str)

    def get_db(self):
        return self.client.ygl


def insert_new_wx_user(_id, data, doctor_openid):
    db = DBHandle()
    root_logger.info(_id)
    root_logger.info(data)
    root_logger.info(doctor_openid)
    db.get_db().wx_user.insert({
        '_id': _id,
        'data': data,
        'doctor_openid': doctor_openid
    })


def test():
    db = DBHandle()
    t = db.get_db().wx_user.find_one()
    print(t)


if __name__ == '__main__':
    insert_new_wx_user('dscd', {}, 'dfd')