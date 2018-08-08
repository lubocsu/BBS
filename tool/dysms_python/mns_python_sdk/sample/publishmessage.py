#!/usr/bin/env python
#coding=utf8

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import time
from sample_common import MNSSampleCommon
from mns.mns_account import Account
from mns.mns_topic import *

#从sample.cfg中读取基本配置信息
## WARNING： Please do not hard code your accessId and accesskey in next line.(more information: https://yq.aliyun.com/articles/55947)
accid,acckey,endpoint,token = MNSSampleCommon.LoadConfig()

#初始化 my_account, my_topic
my_account = Account(endpoint, accid, acckey, token)
topic_name = MNSSampleCommon.LoadIndexParam(1)
if not topic_name:
    print("Error: get parameter failed")
    sys.exit(0)
my_topic = my_account.get_topic(topic_name)

#循环发布多条消息
msg_count = 3
print("%sPublish Message To Topic%s\nTopicName:%s\nMessageCount:%s\n" % (10*"=", 10*"=", topic_name, msg_count))

for i in range(msg_count):
    try:
        msg_body = u"I am test message %s." % i
        msg = TopicMessage(msg_body)
        re_msg = my_topic.publish_message(msg)
        print("Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body, re_msg.message_id))
    except MNSExceptionBase as e:
        if e.type == "TopicNotExist":
            print("Topic not exist, please create it.")
            sys.exit(1)
        print("Publish Message Fail. Exception:%s" % e)
