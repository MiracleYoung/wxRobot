#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/19/18

__author__ = 'MiracleYoung'

import itchat

UNLIMIT_GROUP = []
LIMIT_GROUP = [
    '猿媛牧场1群', '猿媛牧场2群', '淼淼之森', '格姗知识圈群', 'leoay社区', '限时推文', '限推'
]
RESTRICT_GROUP = [
    '禁推文', '禁止推文'
]

FRIEND_ASK_KW = [
    '合作', '商务',
]

AD_KW = ['广告']
PT_KW = ['项目', '有偿', '兼职']

instance = itchat.new_instance()
is_open = False
