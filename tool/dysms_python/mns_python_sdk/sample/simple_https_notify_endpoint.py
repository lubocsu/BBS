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
import ssl
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


RSA_PRIVATE_KEY = u"\n-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC7UKbXif9YkFQAghYs0CEZL066Sy2YbEKHdVm1OqmIHHY9CV9s\nFeCMD9HbbDwsBA2XQsVb7NP5MRydwTCpwCOBpntr0w94PuE+Q8TcLSHxgoqqI29s\nzF0xyRXjAJFabzu2sei8RySLw57C64lWIOxPrWsi+GHQK0XcFU7JfFACIQIDAQAB\nAoGBAKtDfZia2vYN2FAyoLXOgkS1pWTdsc2oRlf16tSx0ynY5B7AgBeiFRHasQTP\nfGC+P/LqIOsAqXsw9Toj1iuOuqaSBYpuCHFMe/dxrEAPXXA7GCMwW3lDeSfMinHV\nrjLTDMhZRLN+jT5QvlkOBNibaZSc3bmCwmGbkEeREkDGD+fFAkEA6A/pQQfT25ip\nAKHh2VOIzfOpiBfC0sci6ZF845kh5GxyFUAeq+hjUUx+ihzI7eIqKrkY+41eYz73\nSGhwuBkmhwJBAM6jGWNv0PgxcLs+sGa55BL53KuiVjIONxOhKrk3OfoF+i8jY7c7\ngUE3kgckcx7FZY323kjGSwX626+jvyRdFBcCQDv9kQEcsun75wSg1K/H5n/HU7Y4\n3kZ68E2NLMnxlk9ksYFI2CT8qGAl9DhkBJVqeBgfTZQKEbJ6Xpa7WRheeBUCQQDE\nS5oFpSYdcFIH/lBy9aodALFJdqhtWqWlhxff5P+1bNIyz2qdmPB7tL+K+2xE0f5c\nMyUMexqv7pOdMW+Vqro3AkAVx3pYn7e1YqMM40jI0J+CqyhXYZ2esiWvBylS+FUN\nY6WOonIAv774LIURaTplcAMuOAj6VDHpVmSDVvnVMgEu\n-----END RSA PRIVATE KEY-----"

CERTIFICATE = u"\n-----BEGIN CERTIFICATE-----\nMIIDbDCCAtWgAwIBAgIJALKoPicL21iaMA0GCSqGSIb3DQEBBQUAMIGBMQswCQYD\nVQQGEwJDTjERMA8GA1UECBMIWmhlamlhbmcxETAPBgNVBAcTCEhhbmd6aG91MQ8w\nDQYDVQQKDAZBbGluCAgxEzARBgNVBAsTCkFwc2FyYSBPU1MxDDAKBgNVBAMTA09T\nUzEYMBYGCSqGSIb3DQEJARYJYWxleC5rcQgIMB4XDTE0MDgyMDA4MjM1NVoXDTE1\nMDgyMDA4MjM1NVowgYExCzAJBgNVBAYTAkNOMREwDwYDVQQIEwhaaGVqaWFuZzER\nMA8GA1UEBxMISGFuZ3pob3UxDzANBgNVBAoMBkFsaW4ICDETMBEGA1UECxMKQXBz\nYXJhIE9TUzEMMAoGA1UEAxMDT1NTMRgwFgYJKoZIhvcNAQkBFglhbGV4LmtxCAgw\ngZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBALtQpteJ/1iQVACCFizQIRkvTrpL\nLZhsQod1WbU6qYgcdj0JX2wV4IwP0dtsPCwEDZdCxVvs0/kxHJ3BMKnAI4Gme2vT\nD3g+4T5DxNwtIfGCiqojb2zMXTHJFeMAkVpvO7ax6LxHJIvDnsLriVYg7E+tayL4\nYdArRdwVTsl8UAIhAgMBAAGjgekwgeYwHQYDVR0OBBYEFMuRh/onWCJ+geGxBp6Y\nMEugx/0HMIG2BgNVHSMEga4wgauAFMuRh/onWCJ+geGxBp6YMEugx/0HoYGHpIGE\nMIGBMQswCQYDVQQGEwJDTjERMA8GA1UECBMIWmhlamlhbmcxETAPBgNVBAcTCEhh\nbmd6aG91MQ8wDQYDVQQKDAZBbGluCAgxEzARBgNVBAsTCkFwc2FyYSBPU1MxDDAK\nBgNVBAMTA09TUzEYMBYGCSqGSIb3DQEJARYJYWxleC5rcQgIggkAsqg+JwvbWJow\nDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOBgQA/8bbaN0Zwb44belQ+OaWj\n7xgn1Bp7AbkDnybpCB1xZGE5sDSkoy+5lNW3D/G5cEQkMYc8g18JtEOy0PPMKHvN\nmqxXUOCSGTmiqOxSY0kZwHG5sMv6Tf0KOmBZte3Ob2h/+pzNMHOBTFFd0xExKGlr\nGr788nh1/5YblcBHl3VEBA==\n-----END CERTIFICATE-----"


def main(ip_addr, port, endpoint_class = server.SimpleHttpNotifyEndpoint, msg_type=u"XML", prefix=u"https://"):
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

    tmpcertfile = "x509_public_certificate_checkhttp.pem"
    tmpkeyfile = "rsa_private_key_checkhttp.pem"
    open(tmpcertfile, 'w').write(CERTIFICATE)
    open(tmpkeyfile, 'w').write(RSA_PRIVATE_KEY)

    #start endpoint
    addr_info = "Start Endpoint! Address: %s%s:%s" % (prefix, ip_addr, port)
    print(addr_info)
    try:
        logger.info(addr_info)
        httpd = HTTPServer((ip_addr, port), endpoint_class)  
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=tmpkeyfile, certfile=tmpcertfile, server_side=True)  
        httpd.serve_forever()  
        #httpd = server.ThreadedHTTPServer(('', port), endpoint_class)
    except KeyboardInterrupt:
        print("Shutting down the simple notify endpoint!")
        httpd.socket.close()

if __name__ == "__main__":
    
    ip_addr = MNSSampleCommon.LoadIndexParam(1)
    if not ip_addr:
        print("ERROR: Must specify IP address")
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
