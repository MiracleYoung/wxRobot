#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

import functools, threading, time
import itchat
from itchat.content import *

import sys, os

print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)

instance = itchat.new_instance()


class FileHelper:
    def __init__(self, instance):
        self.instance = instance
        self.th = threading.Thread(target=self.update_chatrooms, args=())
        self.th.start()

    def update_chatrooms(self):
        while True:
            self.groups = []
            all = self.instance.get_chatrooms()
            for group in all:
                self.groups.append(group.UserName)
            print(len(self.groups))
            time.sleep(30)


@instance.msg_register([FRIENDS], isFriendChat=True)
def friends(res):
    msg = res['Text']
    try:
        # add friends
        if res['MsgType'] == 51 and res['Status'] == 3 and res['StatusNotifyCode'] == 5:
            # TODO
            # add friends
            to_user = res.ToUserName
            instance.add_friend(userName=to_user, status=3)
            instance.send_msg('''
                由于人数已满100，回复：“技术群”，拉你入群。
                知识星球内有「Python原创」、「大航海计划」、「问题解答」、「面试刷题」、「大厂内推」、「技术分享」等，在这个星球能够得到的，不只是关于Python，圈子、人脉、资源，学习氛围，眼界都是比技术更值得去借鉴的东西。
                如果想要加入知识星球的话，可以回复“知识星球”
            ''', to_user=to_user)
            print('已添加好友')
    except AttributeError:
        pass


@instance.msg_register([TEXT], isFriendChat=True)
def auto_reply(res):
    msg = res['Text']
    from_user = res['User']
    if msg == '技术群':
        instance.add_member_into_chatroom(instance.search_chatrooms('测试群2')[0].UserName,
                                          memberList=[from_user])
    elif msg == '知识星球':
        instance.send_image('./textpng.png', toUserName=from_user)
    else:
        pass


fh = FileHelper(instance)

instance.auto_login(hotReload=True)
instance.run()
