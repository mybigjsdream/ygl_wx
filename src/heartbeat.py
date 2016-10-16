#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from conf import HOST_IP, HOST_PORT, root_logger
import requests


def main():
    send_sms_uri = 'http://20.pub.sina.com.cn:18080/add_email_sms'
    sms_content = {
        "coding": "utf-8",
        "id_title": "you-get-video",
        "user": "dengjing",
        "email_alert_span_minutes": "1",
        "email_title": "",
        "email_content": "",
        # "emails": "dengjing@staff.sina.com.cn"
        "emails": "554816284@qq.com"
    }
    url = "http://%s:%s/test" % (HOST_IP, HOST_PORT)
    try:
        r = requests.get(url, timeout=2)
        s = json.loads(r.content.decode('utf-8'))
        print(s)
        if s['status'] != 0:
            raise
    except:
        root_logger.error(u'测试接口不联通')
        sms_content['email_title'] = 'you-get-video接口不通'
        requests.post(send_sms_uri, data=sms_content)


if __name__ == '__main__':
    main()
