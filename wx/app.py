#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/4/8 上午9:14
# @Author  : MiracleYoung
# @File    : app.py


import threading

import requests
import re

import itchat
from itchat.content import TEXT

AD_KW = ['广告']
PT_KW = ['项目', '有偿', '兼职']

instance = itchat.new_instance()
instance.auto_login(hotReload=True, statusStorageDir='./wx_instance.pkl')


@instance.msg_register([TEXT], isGroupChat=True)
def group_filter(msg):
    for kw in PT_KW:
        if kw in msg['Text']:
            from_user = msg['ActualNickName']
            from_group = msg['User']['NickName']
            text = msg['Text']
            instance.send_msg(f'{from_group} 的 {from_user} 发送了一条part time: {text}', toUserName='filehelper')

    return


@instance.msg_register([TEXT], isFriendChat=True)
def file_helper(msg):




if __name__ == '__main__':
    # 微信群组消息
    instance.run()



