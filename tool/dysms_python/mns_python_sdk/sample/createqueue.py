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

#创建队列, 具体属性请参考mns/queue.py中的QueueMeta结构
queue_meta = QueueMeta()
try:
    queue_url = my_queue.create(queue_meta)
    print("Create Queue Succeed! QueueName:%s\n" % queue_name)
except MNSExceptionBase as e:
    if e.type == "QueueAlreadyExist":
        print("Queue already exist, please delete it before creating or use it directly.")
        sys.exit(0)
    print("Create Queue Fail! Exception:%s\n" % e)
