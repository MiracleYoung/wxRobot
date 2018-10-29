#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

__all__ = ['BaseHandle']


class BaseHandle:

    def __init__(self):
        '''
        _meta = {
            'obj':{ # 消息发送对象
                'ul': [], # unlimit group
                'l': [], # limit group
                'r': [] # restrict
            },
            'reply':{
                'text': '',
                'article': '',
            }
        }
        '''
        self._usage = ''
        self._meta = {}
        self.current_cmd = None

    @property
    def usage(self):
        return self._usage

    @property
    def meta(self):
        return self._meta
