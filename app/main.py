#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/10/17 上午6:26

__author__ = 'Miracle'

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from itchat.content import *

from core import fh, friend
from utility import g_is_open
from etc import instance, WX_IMG_DIR, TMP_DIR


@instance.msg_register([FRIENDS], isFriendChat=True)
@g_is_open
def friends(res):
    try:
        # 添加好友
        msg = res['RecommendInfo']['Content']
        username = res['RecommendInfo']['UserName']
        nickname = res['RecommendInfo']['NickName']
        add_ret = instance.add_friend(username, 3)
        if add_ret['BaseResponse']['ErrMsg'] == '请求成功':
            print(f'已添加好友: {nickname}')
            instance.send_msg(friend.meta['extra']['welcome'], username)
            # 修改备注
            # 若有商务、合作等关键字，备注: 商务-
            # 其他备注：Python专栏-
            if friend.is_biz(msg):
                instance.set_alias(username, f'商务-{nickname}')
            else:
                instance.set_alias(username, f'python专栏-{nickname}')
            instance.send_msg(f'添加好友: {nickname} 成功。', 'filehelper')
        else:
            print(f'添加好友失败: {nickname}')

    except Exception:
        pass


@instance.msg_register([TEXT], isFriendChat=True)
@g_is_open
def file_helper(res):
    msg = res['Text']
    from_user = res['FromUserName']
    to_user = res['ToUserName']
    if msg == '技术群':
        instance.send_msg('晚些我会统一拉你们入群～', to_user=from_user)
        return
    if msg == '知识星球':
        instance.send_image(os.path.join(WX_IMG_DIR, 'zsxq.jpeg'), toUserName=from_user['UserName'])
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


if __name__ == '__main__':
    instance.auto_login(
        hotReload=True,
        statusStorageDir=os.path.join(TMP_DIR, 'wx_instance.pkl'),
        picDir=os.path.join(TMP_DIR, 'QR.png')
    )
    instance.run()
