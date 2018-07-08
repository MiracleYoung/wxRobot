#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/4/8 上午9:14
# @Author  : MiracleYoung
# @File    : app.py


import threading

import requests
import re

import itchat
from itchat.content import TEXT

AD_KW = ['广告']
PT_KW = ['项目', '有偿', '兼职']

instance = itchat.new_instance()
instance.auto_login(hotReload=True, statusStorageDir='./wx_instance.pkl')


@instance.msg_register([TEXT], isGroupChat=True)
def group_filter(msg):
    for kw in PT_KW:
        if kw in msg['Text']:
            from_user = msg['ActualNickName']
            from_group = msg['User']['NickName']
            text = msg['Text']
            instance.send_msg(f'{from_group} 的 {from_user} 发送了一条part time: {text}', toUserName='filehelper')

    return


COOKIES = 'noticeLoginFlag=1; ua_id=YVnLJ7KnYkLxVgalAAAAAAopfSjOzWyN7cBb9el36CI=; mm_lang=zh_CN; pgv_pvi=9898065920; pgv_si=s110435328; uuid=58ac9eaa0197540b5584612399baa60c; cert=8TKN8Sq1e3Ityf_Q8F4J0XXemHd26ByR; xid=f1ea101ec9c3e0e3b70c1f7c0f59525b; openid2ticket_ourGaxLLs9mPG-RRBXOSbfh9N-N4=0HhwENGfUOYAG4QvBzMYEEH1QvqKxb/kOK3twQkaWRs=; rewardsn=; mmad_session=d3ac653711a6337d9af26067973ff58b4c6180d14d1f8345e58230a4ca0d8e727701fc2f437fa3e88def3cf730acaea0f41c3e3167cee480ff8d4537792c3eb3081492cd70b868de6b773cea6a06aa0abdb309716c4fffbc22ea5d5de04b497111de1c56c245721266e7088080fefde3; slave_sid=aW16NjBFekVGTmxpZktmWHFsUFRURGpoR24ydVlZdElkMHhaVEJXSWpLZlNaOUlyaHdIeDdWakJlZktlNXdpVlcwOUs3cUVMYXI0V3FCUXhpRHpNSXRUanVwQ0ZQWEIzcUhLTFVCRWtydXZwc3VIRHdHYUYyV0tHUGlpYjdKVVZPTVJrOTlrQThQNzFkOEF1; slave_user=gh_a5fa7c1197fb; data_bizuin=3298472378; data_ticket=xYOvclpg4WvMV0jWOac9tl+HqzghFa4vsoO15bwz3PROL9nXAPbNCLekinT1YDgs; ticket=306b0612cf3e3b993782aedab09061bcc4768f87; ticket_id=gh_a5fa7c1197fb; bizuin=3262473131; slave_user=gh_a5fa7c1197fb; slave_sid=aW16NjBFekVGTmxpZktmWHFsUFRURGpoR24ydVlZdElkMHhaVEJXSWpLZlNaOUlyaHdIeDdWakJlZktlNXdpVlcwOUs3cUVMYXI0V3FCUXhpRHpNSXRUanVwQ0ZQWEIzcUhLTFVCRWtydXZwc3VIRHdHYUYyV0tHUGlpYjdKVVZPTVJrOTlrQThQNzFkOEF1; bizuin=3262473131; pac_uid=0_5b3f87f3e0b1d; pgv_info=ssid=s8267902723; pgv_pvid=9297718389; logout_page=; qm_authimgs_id=2; qm_verifyimagesession=h019f4467c4045d8291297bb62db78bf5b636d3d46d29516c66fec6fd40b961e404de747faeb2c8512d; wxtokenkey=777; sig_login=h01f4247846e49bf3cc1a11c3986826bf8a4ff0492f317f279d71e4dc296fd4933006a0f7a59dd430d5'


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


if __name__ == '__main__':
    # 微信群组消息
    instance.run()
