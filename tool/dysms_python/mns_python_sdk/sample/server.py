#!/usr/bin/env python
#coding=utf8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import cgi
import shutil
import socket
import base64
import logging
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
except Exception as err:
    raise(err)
#import M2Crypto
#from cryptography import x509
#from cryptography.hazmat.primitives import hashes, serialization
#from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives.asymmetric import padding
#import cryptography

import logging.handlers
import xml.dom.minidom
#import BaseHTTPServer
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except Exception as err:
    raise(err)

#import SocketServer
try:
    import socketserver as SocketServer
except ImportError:
    import SocketServer as SocketServer

from sample_common import MNSSampleCommon

__version__ = "1.0.3"
_LOGGER = logging.getLogger(__name__)

#class SimpleHttpNotifyEndpoint(BaseHTTPServer.BaseHTTPRequestHandler):
class SimpleHttpNotifyEndpoint(BaseHTTPRequestHandler):
    server_version = "SimpleHttpNotifyEndpoint/" + __version__
    access_log_file = "access_log"
    msg_type = "XML"

    def do_POST(self):
        #content_length = int(self.headers.getheader('content-length', 0))
        content_length = int(self.headers['content-length'])
        self.req_body = self.rfile.read(content_length)
        self.msg = NotifyMessage()
        _LOGGER.info("Headers:%s\nBody:%s" % (self.headers, self.req_body))
        if not self.authenticate():
            res_code = 403
            res_content = u"Access Forbidden"
            _LOGGER.warning("Access Forbidden!\nHeaders:%s\nReqBody:%s\n" % (self.headers, self.req_body))
        elif not self.validateBody(self.req_body, self.msg, self.msg_type):
            res_code = 400
            res_content = "Invalid Notify Message"
            _LOGGER.warning("Invalid Notify Message!\nHeaders:%s\nReqBody:%s\n" % (self.headers, self.req_body))
        else:
            res_code = 201
            res_content = u""
            _LOGGER.info("Notify Message Succeed!\n%s" % self.msg)
        self.access_log(res_code)
        self.response(res_code, res_content)

    def authenticate(self):
        #get string to signature
        service_str = "\n".join(sorted(["%s:%s" % (k,v) for k,v in self.headers.items() if k.startswith("x-mns-")]))
        sign_header_list = []
        for key in ["content-md5", "content-type", "date"]:
            if key in self.headers.keys():
                sign_header_list.append(self.headers[key])
            else:
                sign_header_list.append("")
        str2sign = u"%s\n%s\n%s\n%s" % (self.command, "\n".join(sign_header_list), service_str, self.path)

        #verify
        #authorization = self.headers.getheader('Authorization')
        authorization = self.headers['Authorization']
        signature = base64.b64decode(authorization)
        cert = urlopen(base64.b64decode(self.headers['x-mns-signing-cert-url']).decode('utf-8')).read()
        cert_str = cert.decode('utf-8')

        from Crypto.Util.asn1 import DerSequence
        from Crypto.PublicKey import RSA 
        from Crypto.Signature import PKCS1_v1_5
        from Crypto.Hash import SHA
        from binascii import a2b_base64

        # Convert from PEM to DER
        lines = cert_str.replace(" ",'').split()
        der = a2b_base64(''.join(lines[1:-1]))
        
        # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
        cert = DerSequence()
        cert.decode(der)
        tbsCertificate = DerSequence()
        tbsCertificate.decode(cert[0])
        subjectPublicKeyInfo = tbsCertificate[6]

        # Initialize RSA key
        key = RSA.importKey(subjectPublicKeyInfo)
        h = SHA.new(str2sign.encode('utf-8'))
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(h, signature):
            return True
        return False


    def validateBody(self, data, msg, type):
        if type == "XML":
            return self.xml_decode(data, msg)
        else:
            msg.message = data
            return True

    def xml_decode(self, data, msg):
        if data == "":
            logger.error("Data is \"\".")
            return False
        try:
            dom = xml.dom.minidom.parseString(data)
        except Exception as e:
            _LOGGER.error("Parse string fail, exception:%s" % e)
            return False

        node_list = dom.getElementsByTagName("Notification")
        if not node_list:
            _LOGGER.error("Get node of \"Notification\" fail:%s" % e)
            return False

        data_dic = {}
        for node in node_list[0].childNodes:
            if node.nodeName != "#text" and node.childNodes != []:
                data_dic[node.nodeName] = node.firstChild.toxml().encode('utf-8')

        key_list = ["TopicOwner", "TopicName", "Subscriber", "SubscriptionName", "MessageId", "MessageMD5", "Message", "PublishTime"]
        for key in key_list:
            if key not in data_dic.keys():
                _LOGGER.error("Check item fail. Need \"%s\"." % key)
                return False

        msg.topic_owner = data_dic["TopicOwner"]
        msg.topic_name = data_dic["TopicName"]
        msg.subscriber = data_dic["Subscriber"]
        msg.subscription_name = data_dic["SubscriptionName"]
        msg.message_id = data_dic["MessageId"]
        msg.message_md5 = data_dic["MessageMD5"]
        msg.message_tag = data_dic["MessageTag"] if data_dic.has_key("MessageTag") else ""
        msg.message = data_dic["Message"]
        msg.publish_time = data_dic["PublishTime"]
        return True

    def response(self, response_code, response_content):
        self.send_response(response_code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(response_content)))
        self.end_headers()
        self.wfile.write(response_content.encode('utf-8'))

    def send_response(self, code, message=None):
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = u''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write((u"%s %d %s\r\n" %
                             (self.protocol_version, code, message)).encode('utf-8'))
            # print (self.protocol_version, code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    def access_log(self, res_code):
        """
        access_log format: time method res_code path req_http_version req_length req_host req_agent mns_reqid mns_version
        """
        item_list = [self.command, res_code, self.path, self.request_version]
        header_key_list = ["Content-Length", "Host", "User-Agent", "x-mns-request-id", "x-mns-version"]
        for key in header_key_list:
            #if self.headers.has_key(key):
            if key in self.headers:
                #item_list.append(self.headers.getheader(key))
                item_list.append(self.headers[key])
            else:
                item_list.append("-")
        acc_log = "[%s]" % self.log_date_time_string() + " ".join(["\"%s\"" % item for item in item_list]) + "\n"
        print(acc_log)
        open(self.access_log_file, 'a').write(acc_log)

#class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
class ThreadedHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
    '''Handle request in a separated thread.'''

class NotifyMessage:
    def __init__(self):
        self.topic_owner = ""
        self.topic_name = ""
        self.subscriber = ""
        self.subscription_name = ""
        self.message_id = ""
        self.message_md5 = ""
        self.message_tag = ""
        self.message = ""
        self.publish_time = -1

    def __str__(self):
        msg_info = {"TopicOwner"    : self.topic_owner,
                    "TopicName"     : self.topic_name,
                    "Subscriber"    : self.subscriber,
                    "SubscriptionName"  : self.subscription_name,
                    "MessageId"     : self.message_id,
                    "MessageMD5"    : self.message_md5,
                    "MessageTag"     : self.message_tag,
                    "Message"       : self.message,
                    "PublishTime"   : self.publish_time}
        return "\n".join(["%s: %s"%(k.ljust(30),v) for k,v in msg_info.items()])


