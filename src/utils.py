# -*- coding: utf-8 -*-
import json

from conf import root_logger, appname
from tornado.httpclient import HTTPClient, HTTPError
from you_get.common import get_html, match1, url_info


def qq_show_url_by_vid(vid):
    api = "http://h5vv.video.qq.com/getinfo?otype=json&platform=10901&vid=%s" % vid
    content = get_html(api)
    output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
    url = output_json['vl']['vi'][0]['ul']['ui'][0]['url']
    fvkey = output_json['vl']['vi'][0]['fvkey']
    mp4 = output_json['vl']['vi'][0]['cl'].get('ci', None)
    if mp4:
        mp4 = mp4[0]['keyid'].replace('.10', '.p') + '.mp4'
    else:
        mp4 = output_json['vl']['vi'][0]['fn']
    url = '%s/%s?vkey=%s' % (url, mp4, fvkey)
    _, ext, size = url_info(url, faker=True)
    return url, ext, size


def get_video_id():
    url = 'http://i.s.video.sina.com.cn/video/getVideoId?appname=%s' % appname
    http_client = HTTPClient()
    try:
        response = http_client.fetch(url)
    except HTTPError as e:
        root_logger.error("Error: %s" % e)
    http_client.close()
    ret_json = json.loads(response.body.decode('utf-8'))
    return ret_json['data']['video_id'], ret_json['data']['token']


if __name__ == '__main__':
    root_logger.info('haha')