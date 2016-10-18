# -*- coding: utf-8 -*-
import json

from conf import root_logger, HOST_IP, HOST_PORT, token, wechat
from model import insert_new_wx_user
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
        data = self.request.body.decode("utf-8")
        wechat.parse_data(data)
        if isinstance(wechat.message, EventMessage):
            if wechat.message.key == 'V0001_MENU':
                root_logger.info(u'点击链接的来源')
                root_logger.info(wechat.message.source)
                articles = [
                    {
                        'title': u'咨询我的医生',
                        'description': u'咨询我的绑定的医生',
                        'picurl': 'http://obsk2aox1.bkt.clouddn.com/78e0ea90-8527-11e6-9164-00163e032929',
                        'url': 'http://m.yigonglue.com:9000/wx/login?user_id=%s' % wechat.message.source,
                        }
                ]
                wechat.send_article_message(wechat.message.source, articles=articles)
            if wechat.message.type == 'scan':
                root_logger.info(u'扫描带的特殊值')
                root_logger.info(wechat.message.key)
                root_logger.info(u'扫描来源')
                root_logger.info(wechat.message.source)
                insert_new_wx_user(
                    wechat.message.source,
                    wechat.get_user_info(wechat.message.source, lang='zh_CN'),
                    wechat.message.key
                )


class WxGetUserHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_argument('user_id')
        doctor_openid = self.get_argument('doctor_openid')
        content = 'http://m.yigonglue.com:9000/wx/chart?role=doctor&wx_user_id=%s' % doctor_openid
        ret_json = wechat.send_text_message(user_id, content)
        self.set_header("Content-Type", "application/json;Charset=utf-8")
        self.finish(json.dumps(ret_json))


class WxSendMessageHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_argument('user_id')
        ret_json = wechat.get_user_info(user_id, lang='zh_CN')
        self.set_header("Content-Type", "application/json;Charset=utf-8")
        self.finish(json.dumps(ret_json))


class WxGetQrcodeHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_argument('user_id')
        data = {
            "action_name": "QR_LIMIT_STR_SCENE",
            "action_info": {
                "scene": {
                    "scene_str": user_id
                }
            }
        }
        ret_json = wechat.create_qrcode(data)
        y_ticket = ret_json['ticket']
        response = wechat.show_qrcode(y_ticket)
        self.set_header('Content-Type', 'image/jpg')
        for chunk in response.iter_content(1024):
            self.write(chunk)
        self.finish()


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        ret_json = {"status": 0}
        root_logger.info(u'测试logger')
        self.set_header("Content-Type", "application/json;Charset=utf-8")
        self.finish(json.dumps(ret_json))


def make_app():
    return tornado.web.Application([
        (r"/wx", WxHandler),
        (r"/wx_get_user", WxGetUserHandler),
        (r"/wx_send_message", WxSendMessageHandler),
        (r"/wx_get_qrcode", WxGetQrcodeHandler),
        (r"/test", TestHandler),
        ])


if __name__ == "__main__":
    app = make_app()
    app.listen(HOST_PORT, address=HOST_IP)
    tornado.ioloop.IOLoop.current().start()