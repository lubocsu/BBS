#!/usr/bin/env python
#coding=utf8

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import time
from sample_common import MNSSampleCommon
from mns.mns_common import *
from mns.mns_account import Account
from mns.mns_topic import *
from mns.mns_subscription import *


ret, params = MNSSampleCommon.LoadParam(4)
if not ret:
    print("Please specify endpoint. e.g. python subscribe_queueendpoint.py cn-hanghzou MySampleSubQueue")
    sys.exit(1)

region = sys.argv[1]
queue_name = sys.argv[2]
topic_name = sys.argv[3]
sub_name = sys.argv[4]


#从sample.cfg中读取基本配置信息
## WARNING： Please do not hard code your accessId and accesskey in next line.(more information: https://yq.aliyun.com/articles/55947)
accid,acckey,endpoint,token = MNSSampleCommon.LoadConfig()
account_id = endpoint.split("/")[2].split(".")[0]
queue_endpoint = TopicHelper.generate_queue_endpoint(region, account_id, queue_name)

#初始化 my_account, my_topic, my_sub
my_account = Account(endpoint, accid, acckey, token)
my_topic = my_account.get_topic(topic_name)

my_sub = my_topic.get_subscription(sub_name)


#创建订阅, 具体属性请参考mns/subscription.py中的SubscriptionMeta结构
sub_meta = SubscriptionMeta(queue_endpoint, notify_content_format = SubscriptionNotifyContentFormat.SIMPLIFIED)
try:
    topic_url = my_sub.subscribe(sub_meta)
    print("Create Subscription Succeed! TopicName:%s SubName:%s Endpoint:%s\n" % (topic_name, sub_name, queue_endpoint))
except MNSExceptionBase as e:
    if e.type == "TopicNotExist":
        print("Topic not exist, please create topic.")
        sys.exit(0)
    elif e.type == "SubscriptionAlreadyExist":
        print("Subscription already exist, please unsubscribe or use it directly.")
        sys.exit(0)
    print("Create Subscription Fail! Exception:%s\n" % e)
