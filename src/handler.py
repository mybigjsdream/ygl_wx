# -*- coding: utf-8 -*-
from conf import wx_conf
from wechat_sdk import WechatBasic


def main():
    wechat = WechatBasic(conf=wx_conf)
    menu_data = {
        'button': [
            {
                'type': 'click',
                'name': '咨询',
                'key': 'V0001_CREATE_MENU'
            }
        ]
    }
    r = wechat.create_menu(menu_data)
    print(r)


if __name__ == '__main__':
    main()