# -*- coding: utf-8 -*-
import json
from conf import mongo_str, root_logger, wechat
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import requests


class DBHandle:
    def __init__(self):
        self.client = MongoClient(mongo_str)

    def get_db(self):
        return self.client.ygl


def insert_new_wx_user(_id, data, doctor_id):
    db = DBHandle()
    base_doctor_data = db.get_db().doctors.find_one({'_id': doctor_id})
    if not base_doctor_data:
        root_logger.error(u"cant find doctor id of %s" % doctor_id)
        return
    doctor_data = {
        '_id': base_doctor_data['_id'],
        'openid': base_doctor_data['_id'],
        'nickname': base_doctor_data['doctorName'],
        'headimgurl': base_doctor_data['avatar']
    }
    try:
        ret = db.get_db().wx_user.insert({
            '_id': _id,
            'data': data,
            'doctor_data': doctor_data
        })
    except DuplicateKeyError:
        root_logger.info(u"插入insert_new_wx_user重复")
        ret = db.get_db().wx_user.update_one(
            {'_id': _id},
            {
                '$set': {'doctor_data': doctor_data}
            }
        )
    root_logger.info(u"插入insert_new_wx_user")
    root_logger.info(ret)


def test():
    db = DBHandle()
    t = db.get_db().wx_user.find_one()
    print(t)


def long2short(long_url, url='https://api.weixin.qq.com/cgi-bin/shorturl', action='long2short'):
    ret = wechat.get_access_token()
    print(ret)
    real_url = url + '?access_token=' + ret['access_token']
    data = {
        'action': action,
        'long_url': long_url
    }
    r = requests.post(real_url, data=json.dumps(data))
    print(r.json())
    return r.json()['short_url']


if __name__ == '__main__':
    # insert_new_wx_user('dscd', {}, 'dfd')
    # print(long2short('https://api.weixin.qq.com/cgi-bin/shorturl', 'long2short', 'http://m.yigonglue.com:9000/wx/chart?role=doctor&wx_user_id=o5JfZshuxFoK1ZCdAZYYt41Bp5gE'))
    print(long2short('http://m.yigonglue.com:9000/wx/chart?role=doctor&wx_user_id=o5JfZshuxFoK1ZCdAZYYt41Bp5gE'))