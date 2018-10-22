#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

__all__ = ['FileHelper']

import functools, random, time, threading

import asyncio

from etc import *


class FileHelper:
    _usage = '''
    '''
    _own = {
        'NickName': 'filehelper',
        'UserName': 'filehelper',
    }

    def __init__(self, instance):
        '''
        _meta = {
            'obj':{ # 消息发送对象
                'ul': [], # unlimit group
                'l': [], # limit group
            },
            'reply':{
                'text': '',
                'article': '',
            }
        }
        '''
        self._meta = {
            'action': {
                'mass': False,
                'friend': False,
            },
            'obj': {
                'ul': [],
                'l': [],
            },
            'reply': {
                'text': '请输入要群发的消息',
                'article': '请输入要群发的文章链接',
            },
            'tmp': ['测试群', '测试群2']
        }
        self._instance = instance
        self._current_cmd = None
        self._th_update = threading.Thread(target=self._update_meta, args=(), daemon=True)
        self._th_update.start()

    def _update_meta(self):
        '''
        初始化限时推送的群组
        '''

        def _filter_groups(self, group):
            for limit in LIMIT_GROUP:
                if limit in group:
                    return True
            return False

        while True:
            print('30s')
            _all = self._instance.get_chatrooms()
            _limits = filter(_filter_groups, _all)
            for limit in _limits:
                self._meta['obj']['ul'].append(limit.UserName)
            # 初始化无限制推送的群组
            self._meta['obj']['l'].extend(list(set(_all) - set(self._meta['obj']['ul'])))
            time.sleep(30)

    def _register_msg(func):
        @functools.wraps(func)
        def decorator(self, msg, *args, **kwargs):
            _action, _reply, _obj = func.__name__.split('_')
            if self._meta['action'][_action]:
                _to_user = self._meta['obj'][_obj]
                for _group in _to_user:
                    self.send_msg(msg, _group)
                    time.sleep(random.randrange(0, 20))
                self._meta['action'][_action] = False
                self._current_cmd = None
                self.send_msg('群发消息发送完毕', self._own['UserName'])
            else:
                self._meta['action'][_action] = True
                self._current_cmd = func.__name__
                self.send_msg(self._meta['reply'][_reply], self._own['UserName'])
            return

        return decorator

    @_register_msg
    def mass_text_ul(self, msg=None):
        pass

    @_register_msg
    def mass_text_l(self, msg):
        pass

    @_register_msg
    def mass_article_ul(self, msg):
        pass

    @_register_msg
    def mass_article_l(self, msg):
        pass

    def send_msg(self, msg, to_user):
        self._instance.send_msg(msg, to_user)

    @property
    def usage(self):
        return self._usage

    @property
    def current_cmd(self):
        return self._current_cmd
