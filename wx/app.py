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
from wx import *
from etc import *

is_open = False  # 全局变量，开启robot开关
instance = itchat.new_instance()
fh = FileHelper(instance)


# @instance.msg_register([TEXT], isGroupChat=True)
# def group_filter(msg):
#     for kw in PT_KW:
#         if kw in msg['Text']:
#             from_user = msg['ActualNickName']
#             from_group = msupdate_metag['User']['NickName']
#             text = msg['Text']
#             instance.send_msg(f'{from_group} 的 {from_user} 发送了一条part time: {text}', toUserName='filehelper')
#
#     return


@instance.msg_register([TEXT], isFriendChat=True)
def file_helper(res):
    global is_open

    msg = res.Text.strip()
    from_user = res.FromUserName
    to_user = res.ToUserName
    if to_user == fh._own['NickName']:
        if msg == 'ro':
            is_open = True
            fh.send_msg('Miracle 微信机器人已开启', to_user)
            return
        if msg == 'rc':
            is_open = False
            fh.send_msg('Miracle 微信机器人已开启', to_user)
            return
        if is_open:
            if msg == 'm':
                return fh.usage
            if fh.current_cmd:
                cmd = f'fh.{fh.current_cmd}'
                eval(cmd)(msg)

            if msg == 'mass text ul':
                return fh.mass_text_ul(msg)
            else:
                return


if __name__ == '__main__':
    instance.auto_login(hotReload=True, statusStorageDir=os.path.join(TMP_DIR, './wx_instance.pkl'))
    instance.run()
