#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'


class WXInit:
    def __init__(self, instance):
        self._meta = {
            'groups': {
                '': None
            },
            'users': []
        }
        for nickname, username in self._meta['groups'].items():
            ret = instance.search_chatrooms(nickname)
            if ret:
                username = self._meta['groups'][0]['UserName']
            else:
                self._meta.pop(nickname)
