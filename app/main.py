#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/4/8 上午9:14
# @Author  : MiracleYoung
# @File    : main.py

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from itchat.content import *

from core import fh, friend
from utility.logger import logger
from utility.misc import g_is_open
from utility.exc import *
from etc import *

is_open = False  # 全局变量，开启robot开关


@instance.msg_register([FRIENDS], isFriendChat=True)
@g_is_open
def friends(res):
    try:
        # 添加好友
        msg = res['RecommendInfo']['Content']
        username = res['RecommendInfo']['UserName']
        nickname = res['RecommendInfo']['NickName']
        friend.add_friend(username, nickname, msg)
    except AddFriend:
        logger.error(f'添加好友失败: {nickname}', exc_info=True)
    except Exception:
        logger.error(f'friends error', exc_info=True)


@instance.msg_register([TEXT], isFriendChat=True)
@g_is_open
def file_helper(res):
    msg = res['Text']
    from_user = res['FromUserName']
    to_user = res['ToUserName']
    if msg == 'm':
        instance.send_msg(fh.usage, from_user)
        return

    if to_user == fh.meta['extra']['NickName']:
        if msg == 'm':
            return fh.usage
        if not fh.current_cmd:
            cmd = '_'.join(msg.split())
            fh.update_cmd(cmd)
            return
        if fh.current_cmd:
            eval(f'fh.{fh.current_cmd}')(msg)
            return
    else:
        # 关键字回复
        friend.kw_reply(msg, from_user)


if __name__ == '__main__':
    instance.auto_login(
        hotReload=True,
        # enableCmdQR=2,
        statusStorageDir=os.path.join(TMP_DIR, 'wx_instance.pkl'),
        picDir=os.path.join(TMP_DIR, 'QR.png')
    )

    instance.run()
