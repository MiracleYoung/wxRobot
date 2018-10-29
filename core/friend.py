#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/24/18

__author__ = 'MiracleYoung'

import os

from core.base import BaseHandle
from utility.logger import logger
from utility.exc import *
from etc.wx_cfg import ADD_FRIENDS_BIZ_KW, instance
from etc.base_cfg import WX_IMG_DIR

__all__ = ['friend']


class Friend(BaseHandle):
    _usage = '''
    
    '''

    def __init__(self):
        super().__init__()
        self._meta = {
            'extra': {
                'ask_kw': ADD_FRIENDS_BIZ_KW,
                'welcome': "由于人数已满100，回复：“技术群”，拉你入群。\n 知识星球内有「Python实战」、「大航海计划」、「大厂内推」、「读书、技术汇」等。\n如果想要加入知识星球的话，可以回复“知识星球”。\n在这个星球能够得到的，不只是关于Python，圈子、人脉、资源、学习氛围、眼界都是比技术更值得去借鉴的东西。\n"
            },
            'kw': {
                'default': lambda: logger.info('错误的关键字'),
                '知识星球': lambda from_user: instance.send_image(os.path.join(WX_IMG_DIR, 'zsxq.jpeg'), from_user),
                '技术群': lambda from_user: instance.send_msg('晚些我会统一拉你们入群～', from_user),
                '谢谢': lambda from_user: instance.send_msg('没事～', from_user)

            }
        }

    def is_biz(self, msg):
        for kw in self._meta['extra']['ask_kw']:
            if kw in msg:
                return True
        return False

    @classmethod
    def set_alias(self, username, nickname, msg=None, prefix=None):
        '''
        修改备注
        若有商务、合作等关键字，备注: 商务-
        其他备注：Python专栏-
        '''
        if prefix:
            instance.set_alias(username, f'{prefix}-{nickname}')
        else:
            if friend.is_biz(msg):
                instance.set_alias(username, f'商务-{nickname}')
            else:
                instance.set_alias(username, f'python专栏-{nickname}')

    def add_friend(self, username, nickname, msg):
        add_ret = instance.add_friend(username, 3)
        if add_ret['BaseResponse']['ErrMsg'] == '请求成功':
            logger.info(f'已添加好友: {nickname}')
            instance.send_msg(friend.meta['extra']['welcome'], username)
            # 修改备注名
            self.set_alias(username, nickname, msg)

            instance.send_msg(f'添加好友: {nickname} 成功。', 'filehelper')
            logger.info(f'添加好友成功: {nickname}')
        else:
            raise AddFriend(f'msg: {msg}, username: {username}, nickname: {nickname}')

    def kw_reply(self, msg, from_user):
        self._meta['kw'].get(msg, 'default')(from_user)


friend = Friend()
