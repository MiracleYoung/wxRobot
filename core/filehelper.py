#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

import functools, time, random, threading, os

from core.base import BaseHandle
from etc.wx_cfg import RESTRICT_GROUP, LIMIT_GROUP, instance
from utility.logger import logger
from utility.exc import *
from core.friend import friend

__all__ = ['fh']


class FileHelper(BaseHandle):
    '''
    object:
        - ul: unlimit
        - l: limit
        - r: restrict
    '''
    _usage = '''
    Miracle wxRobot 操作说明
    ro: 开启机器人
    rc: 关闭机器人
    <action> <type> <object>: 指令集，例如,mass text ul
    action: mass, single
    type: text, article, file, image,
    object: ul, l, r
    alias remark friend: 为联系人设置备注
    
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
                'alias': False,
            },
            'reply': {
                'remark': '请输入备注前缀',
                'text': '请输入要群发的消息',
                'article': '请输入要群发的文章链接',
            },
            'obj': {
                'ul': [],
                'l': [],
                'r': [],
                'test': [],
                'friend': []
            },
        }
        self._th_update = threading.Thread(target=self.update_meta, args=(), daemon=True, name='Thead-UpdateGroup')
        self._th_update.start()
        self._th_round = threading.Thread(daemon=True, name='Thread-Round')

    def _update_meta(self):
        '''
        初始化限时推送的群组
        '''
        _cn = 0

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

        def __update_meta():
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
            finally:
                logger.info(f"Limit group: {len(self._meta['obj']['l'])}, "
                            f"Unlimit group: {len(self._meta['obj']['ul'])}, "
                            f"Restrict group: {len(self._meta['obj']['r'])}")

        __update_meta()

    def update_meta(self):
        while True:
            time.sleep(30)
            # 自动刷新，防止微信掉线
            # _cn += 300
            # if _cn // 1800 == 1:
            #     instance.send_msg('自动刷新', self._meta['extra']['UserName'])
            #     _cn = 0
            self._update_meta()
            time.sleep(270)

    def update_cmd(self, cmd):
        try:
            _action, _reply, _obj = cmd.split('_')
            self._meta['action'][_action] = True
        except (ValueError, KeyError):
            instance.send_msg(f'输入的指令有误，请重新输入.\n {self._usage}', self._meta['extra']['UserName'])
            logger.error(f'cmd is wrong: {cmd}', exc_info=True)
            return
        self.current_cmd = cmd
        instance.send_msg(f"{_action}: {self._meta['reply'][_reply]}", self._meta['extra']['UserName'])

    def _register_mass(func):
        def _mass_msg(msg, to_user):
            for _group in to_user:
                instance.send_msg(msg, _group['UserName'])
                time.sleep(random.randrange(0, 20))

        @functools.wraps(func)
        def decorator(self, msg, *args, **kwargs):
            try:
                _action, _reply, _obj = func.__name__.split('_')
                if self._meta['action'][_action]:
                    # 群发之前先更新群组列表
                    instance.send_msg('开始更新群组列表', self._meta['extra']['UserName'])
                    logger.info('开始更新群组列表')
                    self._update_meta()
                    instance.send_msg('开始群发消息', self._meta['extra']['UserName'])
                    logger.info('开始群发消息')

                    _to_user = self._meta['obj'][_obj]
                    _mass_msg(msg, _to_user)
                    # self._th_send_msg = threading.Thread(target=_send_msg, args=(msg, _to_user), name='Thread-SendMsg')
                    # self._th_send_msg.start()

                    self._meta['action'][_action] = False
                    self._current_cmd = None
                    instance.send_msg('群发消息发送完毕', self._meta['extra']['UserName'])
                    logger.info('群发消息发送完毕')
                else:
                    raise MassMsgError(f"msg: {msg}, split: {func.__name__.split('_')}")
            except MassMsgError:
                instance.send_msg('群发消息失败', self._meta['extra']['UserName'])
                logger.error(f'群发消息失败', exc_info=True)

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

    def alias_remark_friend(self, prefix='python专栏-'):
        try:
            users = [u for u in instance.get_friends() if not u['NickName'].startswith('python专栏')]
            logger.info(f'开始修改备注名')
            for u in users:
                friend.set_alias(u['UserName'], u['NickName'], msg=None, prefix=prefix)
            logger.info(f'修改备注名完成')
        except:
            instance.send_msg('修改备注名失败', self._meta['extra']['UserName'])
            logger.error('修改备注名失败', exc_info=True)


fh = FileHelper()
