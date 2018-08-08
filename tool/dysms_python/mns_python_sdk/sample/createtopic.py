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

#创建主题, 具体属性请参考mns/topic.py中的TopicMeta结构
topic_meta = TopicMeta()
try:
    topic_url = my_topic.create(topic_meta)
    print("Create Topic Succeed! TopicName:%s\n" % topic_name)
except MNSExceptionBase as e:
    if e.type == "TopicAlreadyExist":
        print("Topic already exist, please delete it before creating or use it directly.")
        sys.exit(0)
    print("Create Topic Fail! Exception:%s\n" % e)

