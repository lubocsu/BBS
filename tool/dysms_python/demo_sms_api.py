#!/usr/bin/env python
# coding=utf8
import sys
import datetime
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
from aliyunsdkdybaseapi.request.v20170525.QueryTokenForMnsQueueRequest import QueryTokenForMnsQueueRequest
import const

sys.path.append("./mns_python_sdk/")
from mns.mns_account import Account
from mns.mns_queue import *

try:
    import json
except ImportError:
    import simplejson as json

"""
云通信基础能力业务回执消息消费示例，供参考。

Created on 2017-06-13
Modified on 2017-10-13

"""

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass


# 注意：不要更改
PRODUCT_NAME = "Dybaseapi"
DOMAIN = "dybaseapi.aliyuncs.com"
REGION = "cn-hangzhou"

# TODO 需要替换成您需要接收的消息类型。短信回执：SmsReport，短息上行：SmsUp，语音呼叫：VoiceReport，流量直冲：FlowReport
msgtype = "SmsReport"
# TODO 需要替换成您的队列名称。在云通信页面开通相应业务消息后，就能在页面上获得对应的queueName
qname = "Alicom-Queue-xxxxxx-SmsReport"

# 云通信固定的endpoint地址
endpoint = "https://1943695596114318.mns.cn-hangzhou.aliyuncs.com"

acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# 云通信业务token存在失效时间，需动态更新。
class Token():
    def __init__(self, token=None, tmp_access_id=None, tmp_access_key=None, expire_time=None):
        self.__token = token
        self.__tmp_access_id = tmp_access_id
        self.__tmp_access_key = tmp_access_key
        self.__expire_time = expire_time

    def get_token(self):
        return self.__token

    def set_token(self, token):
        self.__token = token

    def get_tmp_access_id(self):
        return self.__tmp_access_id

    def set_tmp_access_id(self, tmp_access_id):
        self.__tmp_access_id = tmp_access_id

    def get_tmp_access_key(self):
        return self.__tmp_access_key

    def set_tmp_access_key(self, tmp_access_key):
        self.__tmp_access_key = tmp_access_key

    def get_expire_time(self):
        return self.__expire_time

    def set_expire_time(self, expire_time):
        self.__expire_time = expire_time

    def is_refresh(self):
        # 失效时间与当前系统时间比较，提前2分钟刷新token
        now = datetime.datetime.now()
        expire = datetime.datetime.strptime(self.__expire_time, "%Y-%m-%d %H:%M:%S")
        # intval = (expire - now).seconds
        # print "token生效剩余时长（秒）：" + str(intval)
        if expire <= now or (expire - now).seconds < 120:
            return 1
        return 0

    def refresh(self):
        print("start refresh token...")
        request = QueryTokenForMnsQueueRequest()
        request.set_MessageType(msgtype)
		# 数据提交方式
	    # smsRequest.set_method(MT.POST)	
	    # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)
		
        response = acs_client.do_action_with_exception(request)
        # print response
        if response is None:
            raise ServerException("GET_TOKEN_FAIL", "获取token时无响应")

        #response = response.decode('utf-8')
        response_body = json.loads(response.decode('utf-8'))

        if response_body.get("Code") != "OK":
            raise ServerException("GET_TOKEN_FAIL", "获取token失败")

        self.__tmp_access_key = response_body.get("MessageTokenDTO").get("AccessKeySecret")
        self.__tmp_access_id = response_body.get("MessageTokenDTO").get("AccessKeyId")
        self.__expire_time = response_body.get("MessageTokenDTO").get("ExpireTime")
        self.__token = response_body.get("MessageTokenDTO").get("SecurityToken")
        print("key=%s, id=%s, expire_time=%s, token=%s" \
                % (self.__tmp_access_key, self.__tmp_access_id, self.__expire_time, self.__token))

        print("finsh refresh token...")


# 初始化 my_account, my_queue
token = Token()
token.refresh()
my_account = Account(endpoint, token.get_tmp_access_id(), token.get_tmp_access_key(), token.get_token())
my_queue = my_account.get_queue(qname)
# my_queue.set_encoding(False)
# 循环读取删除消息直到队列空
# receive message请求使用long polling方式，通过wait_seconds指定长轮询时间为3秒

## long polling 解析:
### 当队列中有消息时，请求立即返回；
### 当队列中没有消息时，请求在MNS服务器端挂3秒钟，在这期间，有消息写入队列，请求会立即返回消息，3秒后，请求返回队列没有消息；

wait_seconds = 3
print("%sReceive And Delete Message From Queue%s\nQueueName:%s\nWaitSeconds:%s\n" % (
    10 * "=", 10 * "=", qname, wait_seconds))
while True:
    # 读取消息
    try:
        # token过期是否需要刷新
        if token.is_refresh() == 1:
            # 刷新token
            token.refresh()
            my_account.mns_client.close_connection()
            my_account = Account(endpoint, token.get_tmp_access_id(), token.get_tmp_access_key(), token.get_token())
            my_queue = my_account.get_queue(qname)

        # 接收消息
        recv_msg = my_queue.receive_message(wait_seconds)

        # TODO 业务处理
        
        print("Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (
            recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id))
        
    #except MNSExceptionBase as e:
    except Exception as e:
        if e.type == u"QueueNotExist":
            print("Queue not exist, please create queue before receive message.")
            sys.exit(0)
        elif e.type == u"MessageNotExist":
            print("Queue is empty! sleep 10s")
            time.sleep(10)
            continue
        print("Receive Message Fail! Exception:%s\n" % e)
        continue

    # 删除消息
    try:
        my_queue.delete_message(recv_msg.receipt_handle)
        print("Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle)
    except MNSExceptionBase as e:
        print("Delete Message Fail! Exception:%s\n" % e)
