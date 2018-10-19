#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

__all__ = ['FileHelper']

import functools, inspect

from itchat import send_msg

from etc import *


def _reset_status(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        for item in args[0]._meta.values():
            for k, v in item.items():
                if k.startswith('is'):
                    v = False
        return ret

    return wrap


class FileHelper:
    def __init__(self, instance):
        self._meta = {
            'default': {
                'is_default': False,
                'res_text': '默认消息',
            },
            'mass_text': {
                'is_mass_text': False,
                'res_text': '请发送群发内容',
            },
            'mass_article': {
                'is_mass_article': False,
                'res_text': '请发送文章链接',
            }

        }
        self._usage = '''
        
        '''
        self._unlimited_group = []
        self._instance = instance

        for group in self._instance.get_chatrooms():
            if group.NickName:
                self._unlimited_group.append(group.UserName)



    def _send_msg(self, cmd):
        _cmd = '_'.join(cmd.split())
        _item = self._meta.get(_cmd, 'default')
        if _item.get(f'is_{_cmd}', 'is_default'):
            return self._instance._send_msg(msg=_item.get('res_text', ''), toUserName=to_user)
        else:
            _item[f'is_{_cmd}'] = True

    @property
    def usage(self):
        return self._usage

    def mass_article(self, to_user):
        self._send_msg(to_user)

    def mass_text(self, cmd):
        self._send_msg(cmd)

    @_reset_status
    def exec(self, cmd):
        eval(cmd)(cmd)
