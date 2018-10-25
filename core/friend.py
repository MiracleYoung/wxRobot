#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/24/18

__author__ = 'MiracleYoung'

from core.base import BaseHandle
from etc import FRIEND_ASK_KW

__all__ = ['friend']


class Friend(BaseHandle):
    _usage = '''
    
    '''

    def __init__(self):
        super().__init__()
        self._meta = {
            'extra': {
                'ask_kw': FRIEND_ASK_KW,
                'welcome': "由于人数已满100，回复：“技术群”，拉你入群。\n 知识星球内有「Python实战」、「大航海计划」、「大厂内推」、「读书、技术汇」等。\n在这个星球能够得到的，不只是关于Python，圈子、人脉、资源、学习氛围、眼界都是比技术更值得去借鉴的东西。\n如果想要加入知识星球的话，可以回复“知识星球”"
            },
        }

    def is_biz(self, msg):
        for kw in self._meta['extra']['ask_kw']:
            if kw in msg:
                return True
        return False


friend = Friend()
