# -*- coding: utf-8 -*-
import logging

appname = "cms_spider_video"

LOGGING_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    level=logging.NOTSET,
    format=LOGGING_FORMAT,
    datefmt=DATE_FORMAT
)
root_logger = logging.getLogger()


# 数据库配置
# DBSTR = 'sqlite:///../db/test.db'
DBSTR = 'sqlite:////data1/you-get-video/db/you-get.db'
DBARGS = {'echo': False, 'echo_pool': False, 'encoding': 'UTF-8'}

HOST_IP = '172.16.7.21'
HOST_PORT = '8888'