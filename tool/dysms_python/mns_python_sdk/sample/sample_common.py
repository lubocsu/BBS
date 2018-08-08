#!/usr/bin/env python
#coding=utf8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os
import time
try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

class MNSSampleCommon:

    @staticmethod
    def LoadConfig():
        cfg_fn = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/../sample.cfg")
        required_ops = [("Base", "AccessKeyId"), ("Base", "AccessKeySecret"), ("Base", "Endpoint")]
        optional_ops = [("Optional", "SecurityToken")]

        parser = ConfigParser.ConfigParser()
        parser.read(cfg_fn)
        for sec,op in required_ops:
            if not parser.has_option(sec, op):
                sys.stderr.write("ERROR: need (%s, %s) in %s.\n" % (sec,op,cfg_fn))
                sys.stderr.write("Read README to get help inforamtion.\n")
                sys.exit(1)

        accessKeyId = parser.get("Base", "AccessKeyId")
        accessKeySecret = parser.get("Base", "AccessKeySecret")
        endpoint = parser.get("Base", "Endpoint")
        securityToken = ""
        if parser.has_option("Optional", "SecurityToken") and parser.get("Optional", "SecurityToken") != "$SecurityToken":
            securityToken = parser.get("Optional", "SecurityToken")
            return accessKeyId,accessKeySecret,endpoint,securityToken

        return accessKeyId,accessKeySecret,endpoint,""

    @staticmethod
    def LoadParam(params_num):
        # The @topic_name is a bytes-stream on Python2, while it is a unicode-string on Python2.
        # So we must call @decode to decode bytes-stream to unicode-string when runing on Python2.
        # In addition, python3 has NOT @decode Attribute, so igonre the exception when runing on Python3.
        if params_num < len(sys.argv):
            params = list()
            hasdecode = hasattr(sys.argv[1], 'decode')
                
            for p in sys.argv[1:params_num+1]:
                if hasdecode:
                    params.append(p.decode('utf-8'))
                else:
                    params.append(p)

            return params_num, params
        else:
            return 0, None

    @staticmethod
    def LoadIndexParam(index):
        # The @topic_name is a bytes-stream on Python2, while it is a unicode-string on Python2.
        # So we must call @decode to decode bytes-stream to unicode-string when runing on Python2.
        # In addition, python3 has NOT @decode Attribute, so igonre the exception when runing on Python3.
        if index < len(sys.argv):
            if hasattr(sys.argv[1], 'decode'):
                return sys.argv[index].decode('utf-8')
            else:
                return sys.argv[index]
        else:
            return None
