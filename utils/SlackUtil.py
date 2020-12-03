#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import slack

from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
import common.Constant as Const


class SlackUtil:
    def __init__(self):
        self.assert_util = AssertUtil()
        self.slack_token = "xxx"
        self.log = my_log("SlackUtil")
        self.exec_modular = getattr(Const.GetConst(), "EXEC_MODULAR")

    def sendresult(self):
        content = "接口测试结果新鲜出炉，<http://192.168.1.xx:xxxx/view/test_view/|点击前往查看报告>"
        self.send(content)

    def sendpass(self):
        content = "[通过]%s接口测试已通过，<http://192.168.1.xx:xxxx/view/test_view/|点击前往查看报告>" % self.exec_modular
        self.send(content)

    def sendfail(self):
        content = "[未通过]%s接口测试报错啦，<http://192.168.1.xx:xxxx/view/test_view/|快去看看吧！>" % self.exec_modular
        self.send(content)

    def send(self, content):
        client = slack.WebClient(self.slack_token)
        response = client.chat_postMessage(
            channel='xxx',  # slack的channel的link
            text=content
        )

        try:
            assert response["ok"]
        except:
            self.log.error("slack消息发送失败")


if __name__ == '__main__':
    # sendpass()
    SlackUtil().sendfail()
    a = "aaa"

