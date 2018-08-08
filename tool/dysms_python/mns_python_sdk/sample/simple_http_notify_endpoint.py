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
import server

__version__ = "1.0.3"
_LOGGER = logging.getLogger(__name__)

def main(ip_addr, port, endpoint_class = server.SimpleHttpNotifyEndpoint, msg_type=u"XML", prefix=u"http://"):
    #init logger
    global logger
    endpoint_class.access_log_file = "access_log.%s" % port
    endpoint_class.msg_type = msg_type
    log_file = "endpoint_log.%s" % port
    logger = logging.getLogger()
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=100*1024*1024)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(thread)d] %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    #start endpoint
    addr_info = "Start Endpoint! Address: %s%s:%s" % (prefix, ip_addr, port)
    print(addr_info)
    try:
        logger.info(addr_info)
        httpd = server.ThreadedHTTPServer(('', port), endpoint_class)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the simple notify endpoint!")
        httpd.socket.close()

if __name__ == "__main__":
    ip_addr =  MNSSampleCommon.LoadIndexParam(1)
    if not ip_addr:
        print("ERROR: Must specify IP Address")
        sys.exit(0)

    para_port = MNSSampleCommon.LoadIndexParam(2)
    if para_port:
        port = int(para_port)
    else:
        port = 8080
    msg_type = MNSSampleCommon.LoadIndexParam(3)
    if not msg_type:
        msg_type = u"XML"    
    main(ip_addr, port, server.SimpleHttpNotifyEndpoint, msg_type)
