#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/26/18

__author__ = 'MiracleYoung'


class WXException(Exception):
    pass


class ContactError(WXException):
    pass


class AddFriend(ContactError):
    pass


class MsgError(WXException):
    pass


class MassMsgError(MsgError):
    pass


class CMDError(WXException):
    pass
