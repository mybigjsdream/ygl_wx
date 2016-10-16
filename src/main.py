# -*- coding: utf-8 -*-
import json

from conf import root_logger, HOST_IP, HOST_PORT
# from model import VideoInfo, DBSession

# from utils_asyn import asyn_download_video
# from utils import qq_show_url_by_vid, get_video_id
import tornado.ioloop
import tornado.web


class AsynHandler(tornado.web.RequestHandler):
    def get(self):
        ret_json = {"status": 0}
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