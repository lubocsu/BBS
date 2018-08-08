#!/usr/bin/env python
#coding=utf8

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import time
from sample_common import MNSSampleCommon
from mns.mns_account import Account
from mns.mns_queue import *

#从sample.cfg中读取基本配置信息
## WARNING： Please do not hard code your accessId and accesskey in next line.(more information: https://yq.aliyun.com/articles/55947)
accid,acckey,endpoint,token = MNSSampleCommon.LoadConfig()

#初始化 my_account, my_queue
my_account = Account(endpoint, accid, acckey, token)
queue_name = MNSSampleCommon.LoadIndexParam(1)
if not queue_name:
    print("Error: get parameter failed")
    sys.exit(0)
my_queue = my_account.get_queue(queue_name)

#循环发送多条消息
msg_count = 3

print("%sSend Message To Queue%s\nQueueName:%s\nMessageCount:%s\n" % (10*"=", 10*"=", queue_name, msg_count))
for i in range(msg_count):
    try:
        msg_body = u"I am test: %s." % i
        msg = Message(msg_body)
        re_msg = my_queue.send_message(msg)
        print("Send Message Succeed! MessageBody:%s MessageID:%s" % (msg_body, re_msg.message_id))
    except MNSExceptionBase as e:
        if e.type == "QueueNotExist":
            print("Queue not exist, please create queue before send message.")
            sys.exit(0)
        print("Send Message Fail! Exception:%s\n" % e)
