#!/usr/bin/env python
#coding=utf8

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import time
from sample_common import MNSSampleCommon
from mns.mns_account import Account
from mns.mns_topic import *
from mns.mns_subscription import *

#参数合法性检查，订阅的Endpoint参数必须传入
sub_endpoint = MNSSampleCommon.LoadIndexParam(1)
if not sub_endpoint:
    print("Please specify endpoint. e.g. python subscribe.py http://127.0.0.1:80")
    sys.exit(1)

#从sample.cfg中读取基本配置信息
## WARNING： Please do not hard code your accessId and accesskey in next line.(more information: https://yq.aliyun.com/articles/55947)
accid,acckey,endpoint,token = MNSSampleCommon.LoadConfig()

#初始化 my_account, my_topic, my_sub
my_account = Account(endpoint, accid, acckey, token)

topic_name = MNSSampleCommon.LoadIndexParam(2)
if not topic_name:
    topic_name = "MySampleTopic"
my_topic = my_account.get_topic(topic_name)

sub_name = MNSSampleCommon.LoadIndexParam(3)
if not sub_name:
    sub_name = "MySampleTopic-Sub"
my_sub = my_topic.get_subscription(sub_name)

print(sub_endpoint, topic_name, sub_name)

#创建订阅, 具体属性请参考mns/subscription.py中的SubscriptionMeta结构
sub_meta = SubscriptionMeta(sub_endpoint)
try:
    topic_url = my_sub.subscribe(sub_meta)
    print("Create Subscription Succeed! TopicName:%s SubName:%s Endpoint:%s\n" % (topic_name, sub_name, sub_endpoint))
except MNSExceptionBase as e:
    if e.type == "TopicNotExist":
        print("Topic not exist, please create topic.")
        sys.exit(0)
    elif e.type == "SubscriptionAlreadyExist":
        print("Subscription already exist, please unsubscribe or use it directly.")
        sys.exit(0)
    print("Create Subscription Fail! Exception:%s\n" % e)
