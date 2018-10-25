#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

import functools, time, random, threading

from core.base import BaseHandle
from etc import RESTRICT_GROUP, LIMIT_GROUP, instance

__all__ = ['fh']


class FileHelper(BaseHandle):
    _usage = '''
    '''

    def __init__(self):
        super().__init__()
        self._meta = {
            'extra': {
                'NickName': 'filehelper',
                'UserName': 'filehelper',
            },
            'action': {
                'mass': False,
                'friend': False,
            },
            'obj': {
                'ul': [],
                'l': [],
                'r': [],
                'test': []
            },
            'reply': {
                'text': '请输入要群发的消息',
                'article': '请输入要群发的文章链接',
            }
        }
        self._th_update = threading.Thread(target=self._update_meta, args=(), daemon=True)
        self.auto_update_groups()

    def auto_update_groups(self):
        self._th_update.start()

    def _update_meta(self):
        '''
        初始化限时推送的群组
        '''

        def _filter_restrict_groups(group):
            for limit in RESTRICT_GROUP:
                if limit in group['NickName']:
                    return True
            return False

        def _filter_limit_groups(group):
            for limit in LIMIT_GROUP:
                if limit in group['NickName']:
                    return True
            return False

        def _filter_unlimit_group(groups, limit_groups):
            ret = []
            for group in groups:
                for lg in limit_groups:
                    if group['NickName'] == lg['NickName']:
                        break
                else:
                    ret.append(group)
            return ret

        while True:
            time.sleep(30)
            try:
                _all = instance.get_chatrooms(update=True)
                self._meta['obj']['l'] = list(filter(_filter_limit_groups, _all))
                self._meta['obj']['r'] = list(filter(_filter_restrict_groups, _all))
                self._meta['obj']['ul'] = _filter_unlimit_group(
                    _all, self._meta['obj']['l'] + self._meta['obj']['r']
                )
                self._meta['obj']['test'] = [instance.search_chatrooms(group)[0] for group in ['测试群', '测试群2']]
            except Exception:
                self._meta['obj']['l'] = []
                self._meta['obj']['ul'] = []
                self._meta['obj']['r'] = []

            print(len(self._meta['obj']['ul']))

    def update_cmd(self, cmd):
        _action, _reply, _obj = cmd.split('_')
        self._meta['action'][_action] = True
        self.current_cmd = cmd
        instance.send_msg(self._meta['reply'][_reply], self._meta['extra']['UserName'])

    def _register_mass(func):
        @functools.wraps(func)
        def decorator(self, msg, *args, **kwargs):
            _action, _reply, _obj = func.__name__.split('_')
            if self._meta['action'][_action]:
                _to_user = self._meta['obj'][_obj]
                for _group in _to_user:
                    instance.send_msg(msg, _group['UserName'])
                    time.sleep(random.randrange(0, 20))
                self._meta['action'][_action] = False
                self._current_cmd = None
                instance.send_msg('群发消息发送完毕', self._meta['extra']['UserName'])

        return decorator

    @_register_mass
    def mass_text_ul(self, msg=None):
        pass

    @_register_mass
    def mass_text_l(self, msg):
        pass

    @_register_mass
    def mass_text_test(self, msg):
        pass

    @_register_mass
    def mass_article_ul(self, msg):
        pass

    @_register_mass
    def mass_article_l(self, msg):
        pass


fh = FileHelper()
