#! /usr/bin/env python
# -*-coding:utf-8 -*-

"""
@author:Xiuzhu
@file:TextScan.py
@time:2017/12/22 10:27
"""


from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20170112 import TextScanRequest
import json
import uuid
import datetime
import codecs
import time

import ConfigParser



class Connect:
    def __init__(self):
        self.config_name = 'aliyun.ak.conf'

    def get_config(self):
        filename = self.config_name
        cf = ConfigParser.ConfigParser()
        cf.read(filename)
        clt = client.AcsClient(cf.get("AK", "accessKeyId"), cf.get("AK", "accessKeySecret"), 'cn-shanghai')
        return clt

    def connect(self):
        region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
        request = TextScanRequest.TextScanRequest()
        request.set_accept_format('JSON')
        return request


class TextScan:
    def __init__(self,filename = '', text = ''):
        self.text = ''
        if filename != '':
            data = codecs.open(filename, 'r', 'gbk', errors='ignore')
            self.text = data.read()
        if text != '':
            self.text = text

    def __run(self,request,clt):

        task1 = {"dataId": str(uuid.uuid1()),
                 "content": self.text,
                 "time": datetime.datetime.now().microsecond
                 }

        request.set_content(bytearray(json.dumps({"tasks": [task1], "scenes": ["antispam"]}), "utf-8"))
        response = clt.do_action_with_exception(request)
        result = json.loads(response)
        return result

    def get_result(self,reqeust,clt):
        result = self.__run(reqeust,clt)
        result_para = []
        if 200 == result["code"]:
            taskResults = result["data"]
            for taskResult in taskResults:
                if (200 == taskResult["code"]):
                    sceneResults = taskResult["results"]

                    for sceneResult in sceneResults:
                        scene = sceneResult["scene"]
                        label = sceneResult['label']
                        suggestion = sceneResult["suggestion"]

                        result_p = {'scene': scene,
                               'label': label,
                               'suggestion': suggestion}
                        result_para.append(result_p)
        return result_para





if __name__ == "__main__":
    start = time.time()
    connect = Connect()
    clt = connect.get_config()
    request = connect.connect()

    path = r'bad_1.txt'
    result_para = TextScan(filename=path).get_result(request,clt)

