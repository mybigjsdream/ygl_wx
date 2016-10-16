# -*- coding: utf-8 -*-
import logging
from wechat_sdk import WechatConf


appname = "cms_spider_video"
token = "dengjing"

LOGGING_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    level=logging.NOTSET,
    format=LOGGING_FORMAT,
    datefmt=DATE_FORMAT
)
root_logger = logging.getLogger()


wx_conf = WechatConf(
    token='your_token',
    appid='your_appid',
    appsecret='your_appsecret',
    encrypt_mode='safe',
    encoding_aes_key='your_encoding_aes_key'
)


# 数据库配置
# DBSTR = 'sqlite:///../db/test.db'
# DBSTR = 'sqlite:////data1/you-get-video/db/you-get.db'
# DBARGS = {'echo': False, 'echo_pool': False, 'encoding': 'UTF-8'}

# HOST_IP = '172.16.7.21'
HOST_IP = '0.0.0.0'
HOST_PORT = '8888'
# HOST_PORT = '80'