# -*- coding: utf-8 -*-
import json

from conf import root_logger, HOST_IP, HOST_PORT
from model import VideoInfo, DBSession

from utils_asyn import asyn_download_video
from utils import qq_show_url_by_vid, get_video_id
import tornado.ioloop
import tornado.web


class AsynHandler(tornado.web.RequestHandler):
    def get(self):
        vid = self.get_argument('arg')
        session = DBSession()
        video_infos = session.query(VideoInfo).filter(VideoInfo.v_id == vid).all()
        if len(video_infos) > 0:
            root_logger.info(u'%s 在数据库中存在 %s' % (vid, video_infos))
            video_info = video_infos[0]
            ret_json = {
                'ext': video_info.video_ext,
                'size': video_info.video_size,
                'vtype': video_info.v_type,
                'video_id': video_info.sina_video_id,
                'sina_video_url': video_info.sina_video_url
            }
        else:
            url, ext, size = qq_show_url_by_vid(vid)
            ret_json = {"ext": ext, "size": size, "vid": vid, "vtype": "qq"}
            video_id, token = get_video_id()
            ret_json['video_id'] = video_id
            ret_json['sina_video_url'] = "http://video.sina.com.cn/view/%s.html" % video_id
            asyn_download_video(video_id, token, vid, url, ext, size, 'qq')
            root_logger.info(u'打印 %s 的返回 %s' % (vid, ret_json))
            tmp_video = VideoInfo(
                v_id=vid,
                v_type=ret_json['vtype'],
                video_size=ret_json['size'],
                video_ext=ret_json['ext'],
                sina_video_id=ret_json['video_id'],
                sina_video_url=ret_json['sina_video_url']
            )
            session.add(tmp_video)
            session.commit()
        session.close()
        self.set_header("Content-Type", "application/json;Charset=utf-8")
        self.finish(json.dumps(ret_json))


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        ret_json = {"status": 0}
        root_logger.info(u'测试logger')
        self.set_header("Content-Type", "application/json;Charset=utf-8")
        self.finish(json.dumps(ret_json))


def make_app():
    return tornado.web.Application([
        (r"/asyn_api", AsynHandler),
        (r"/test", TestHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(HOST_PORT, address=HOST_IP)
    tornado.ioloop.IOLoop.current().start()