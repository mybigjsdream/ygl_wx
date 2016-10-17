# -*- coding: utf-8 -*-
from conf import wx_conf, wechat
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


def handle_menu():
    del_menu()
    create_menu()


def handle_qr(s):
    data = {
        "action_name": "QR_LIMIT_SCENE",
        "action_info": {
            "scene": {
                "scene_id": s
            }
        }
    }
    r = wechat.create_qrcode(data)
    print(r)  # gQH38DoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xLzVVbG4tYlRrbTE3aUhPLXQyMlVnAAIEXZUEWAMEAAAAAA==


if __name__ == '__main__':
    # handle_menu()
    handle_qr('o5JfZshuxFoK1ZCdAZYYt41Bp5gE')
