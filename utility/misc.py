#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/24/18

__author__ = 'MiracleYoung'

import functools

from etc import instance, is_open

__all__ = ['g_is_open']


def g_is_open(fn):
    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
        res = args[0]
        global is_open
        msg = res['Text']
        to_user = res['ToUserName']
        if msg == 'ro':
            is_open = True
            instance.send_msg('Miracle 微信机器人已开启', to_user)
            return
        if msg == 'rc':
            is_open = False
            instance.send_msg('Miracle 微信机器人已开启', to_user)
            return
        if is_open:
            return fn(*args, **kwargs)
        else:
            instance.send_msg(f'请发送指令：ro，打开机器人', to_user)
            return

    return _wrapper
