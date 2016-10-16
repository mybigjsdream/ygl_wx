# -*- coding: utf-8 -*-
import json
import urllib

from conf import root_logger, appname
import os
import requests
from tornado.httpclient import AsyncHTTPClient


def asyn_download_video(video_id, token, vid, url, ext, size, v_type):
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.abspath(os.path.join(file_path, '../../you-get-video/media/' + v_type + '/' + vid + '.' + ext))
    http_client = AsyncHTTPClient()
    root_logger.info(u'准备下载 %s' % vid)

    def handle_response(response):
        with open(file_name, 'wb') as fi:
            fi.write(response.body)
        asyn_upload_video(video_id, token, file_name, vid, size, ext, v_type)

    http_client.fetch(url, callback=handle_response)
    return file_name


def asyn_upload_video(video_id, token, file_name, vid, size, ext, v_type):
    http_client2 = AsyncHTTPClient()
    url = 'http://i.s.video.sina.com.cn/video/create'
    root_logger.info(u'准备异步上传 %s' % vid)
    post_data = {
        "appname": appname,
        "video_id": video_id,
        "token": token,
        "title": vid + '-' + v_type,
        "file_name": vid + '.' + ext,
        "file_size": size,
        "source": v_type,
        "account_id": 6340,
        "page_status": 1
    }
    body = urllib.parse.urlencode(post_data)

    def handle_response2(response2):
        root_logger.info(u'开始准备上传 %s' % vid)
        i = 0
        while (not os.path.isfile(file_name)) or (size != os.path.getsize(file_name)):
            root_logger.info('heart beat %s' % vid)
            i += 1
            if i > 100:
                break
            else:
                continue
        root_logger.info(u'正式上传 %s' % vid)
        ret_json2 = json.loads(response2.body.decode('utf-8'))
        # root_logger.info(ret_json2)
        url3 = ret_json2['data']['upload_url']
        root_logger.info(u'上传 %s 接口的返回 %s' % (vid, ret_json2))
        r = requests.post(url3, files={'file': open(file_name, 'rb'), 'source': v_type})
        root_logger.info(u'上传完成 %s' % vid)
        r_j = json.loads(r.content.decode('utf-8'))
        root_logger.info(u'%s 的最后打印 %s' % (vid, r_j))

    http_client2.fetch(url, body=body, method='POST', callback=handle_response2)


if __name__ == '__main__':
    asyn_download_video('g0324cns2ck', "http://api.oforever.net:8888/api/index", 3538, 'txt')