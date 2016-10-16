# -*- coding: utf-8 -*-
import json

from conf import root_logger, HOST_IP, HOST_PORT, token, wechat
from wechat_sdk.messages import EventMessage
import tornado.ioloop
import tornado.web
import hashlib


class WxHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            self.finish(echostr)
        else:
            self.finish(echostr)

    def post(self, *args, **kwargs):
        root_logger.info(self.request.body)
        data = self.request.body.decode("utf-8")
        wechat.parse_data(data)
        if isinstance(wechat.message, EventMessage):
            root_logger.info(wechat.message)


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        ret_json = {"status": 0}
        root_logger.info(u'测试logger')
        self.set_header("Content-Type", "application/json;Charset=utf-8")
        self.finish(json.dumps(ret_json))


def make_app():
    return tornado.web.Application([
        (r"/wx", WxHandler),
        (r"/test", TestHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(HOST_PORT, address=HOST_IP)
    tornado.ioloop.IOLoop.current().start()