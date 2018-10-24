#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/10/17 上午6:26

__author__ = 'Miracle'

import re

import requests


class Moment:
    def __init__(self, token, cookie, accounts):
        # token: 750784052
        self._token = token
        self._cookie = self.__extract_strck2dictck(cookie)
        self._urls = {
            'get_fakeid': 'https://mp.weixin.qq.com/cgi-bin/searchbiz',
            'get_articles_list': 'https://mp.weixin.qq.com/cgi-bin/appmsg',
            'get_article_comments': 'https://mp.weixin.qq.com/mp/appmsg_comment'
        }
        self._params = {
            "lang": "zh_CN",
            "f": "json",
        }
        self._session = requests.Session()
        self._headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7',
            # 'Connection': 'keep-alive',
            # 'Host': 'mp.weixin.qq.com',
            # 'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=358402574&lang=zh_CN',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 micromessage Safari/604.1',
            # 'X-Requested-With': 'XMLHttpRequest'
        }
        self._session.headers.update(self._headers)
        # {'xpchuiit': 'fakeid', ...}
        # fakeid: MzI2MjQ3MzEzMQ==
        self._accounts = {account: self.__get_fakeid(account) for account in accounts}

    def __get_fakeid(self, account):
        params = {
            'action': 'search_biz',
            'token': self._token,
            'query': account,
            "ajax": "1",
            'begin': 0,
            'count': 5
        }
        params.update(self._params)
        return self._session.request('GET', self._urls['get_fakeid'], params=params,
                                     cookies=self._cookie).json()['list'][0]['fakeid']

    def __extract_strck2dictck(self, ck):
        return {kv.strip().split('=', 1)[0]: kv.strip().split('=', 1)[1] for kv in ck.split(';')}

    def __get_articles_list(self, fakeid):
        params = {
            'fakeid': fakeid,
            'token': self._token,
            'action': 'list_ex',
            'begin': 0,
            'count': 5,
            'query': '',
            'type': 9
        }
        params.update(self._params)
        return self._session.request('GET', self._urls['get_articles_list'], params=params).json()['app_msg_list']

    def __get_comment_id(self, link):
        # appid, link = article['appmsgid'], article['link']
        payload = {
            "is_only_read": "1",
            "is_temp_url": "0",
        }
        pattern = 'comment_id = "(?P<comment_id>\d+)"'
        m = re.compile(pattern)
        res = self._session.request('GET', link, json=payload).text
        return m.search(res).groupdict()['comment_id']

    def __get_url_params(self, link):
        # link: https://mp.weixin.qq.com/s?__biz=MzI2MjQ3MzEzMQ==&mid=2247484165&idx=1&sn=dc5396655c25aa8c885b9480052b967a&chksm=ea4bd7c1dd3c5ed7788a01f0b310b5163c262db009d9a7ce9ae64545103f96ed52951fefb0fc#rd
        params = link.split('?', 1)[1].split('&')
        return {p.split('=', 1)[0]: p.split('=', 1)[1] for p in params}

    def get_latest_article(self, fakeid):
        return self.__get_articles_list(fakeid)[0]

    def get_comments(self, link):
        comment_id = self.__get_comment_id(link)
        url_params = self.__get_url_params(link)
        params = {
            'action': 'getcomment',
            '__biz': url_params['__biz'],
            'idx': url_params['idx'],
            'comment_id': comment_id,
            'limit': 100
        }
        params.update(self._params)
        return self._session.request('GET', self._urls['get_article_comments'], params=params)
