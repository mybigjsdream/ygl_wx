# -*- coding: utf-8 -*-
from conf import mongo_str, root_logger
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class DBHandle:
    def __init__(self):
        self.client = MongoClient(mongo_str)

    def get_db(self):
        return self.client.ygl


def insert_new_wx_user(_id, data, doctor_openid):
    db = DBHandle()
    try:
        ret = db.get_db().wx_user.insert({
            '_id': _id,
            'data': data,
            'doctor_openid': doctor_openid
        })
    except DuplicateKeyError:
        root_logger.info(u"插入insert_new_wx_user重复")
        ret = db.get_db().wx_user.update_one(
            {'_id': _id},
            {
                '$set': {'doctor_openid': doctor_openid}
            }
        )
    root_logger.info(u"插入insert_new_wx_user")
    root_logger.info(ret)


def test():
    db = DBHandle()
    t = db.get_db().wx_user.find_one()
    print(t)


if __name__ == '__main__':
    insert_new_wx_user('dscd', {}, 'dfd')