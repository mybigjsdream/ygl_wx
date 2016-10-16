# -*- coding: utf-8 -*-
from conf import wx_conf
from wechat_sdk import WechatBasic


def create_menu():
    wechat = WechatBasic(conf=wx_conf)
    menu_data = {
        'button': [
            {
                'type': 'click',
                'name': '咨询',
                # 'url': 'http://m.yigonglue.com:9000/wx/login'
                'key': 'V0001_MENU'
            }
        ]
    }
    r = wechat.create_menu(menu_data)
    print(r)


def del_menu():
    wechat = WechatBasic(conf=wx_conf)
    r = wechat.delete_menu()
    print(r)


if __name__ == '__main__':
    del_menu()
    create_menu()