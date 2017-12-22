#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:Xiuzhu
@file:ImgScan.py
@time:2017/12/22 11:32
"""

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20170112 import ImageSyncScanRequest
import json
import uuid
import datetime
import time
import ConfigParser
from TextScan import TextScan



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
        request = ImageSyncScanRequest.ImageSyncScanRequest()
        request.set_accept_format('JSON')
        return request

class ImageScan:
    def __init__(self,urls = []):
        self.urls = []
        if len(urls) != 0:
            self.urls = urls
        else:
            print "please input image url"


    def __getTask(self):
        task = []

        for url in self.urls:
            task1 = {"dataId": str(uuid.uuid1()),
                     "url": url,
                     "time": datetime.datetime.now().microsecond
                     }
            task.append(task1)
        return task

    def __run(self, request, clt):
        task = self.__getTask()
        request.set_content(bytearray(json.dumps({"tasks": task, "scenes": ["ad","ocr"]}), "utf-8"))
        response = clt.do_action_with_exception(request)
        result = json.loads(response)
        return result

    def get_result(self,reqeust,clt):
        result = self.__run(reqeust,clt)
        if 200 == result["code"]:
            taskResults = result["data"]
            for taskResult in taskResults:
                if (200 == taskResult["code"]):
                    sceneResults = taskResult["results"]

                    for sceneResult in sceneResults:
                        scene = sceneResult["scene"]
                        suggestion = sceneResult["suggestion"]
                        label = sceneResult["label"]
                        print "{'scene':%s,'label':%s,'suggestion':%s}" % (scene, label, suggestion)




if __name__ == "__main__":
    start = time.time()
    connect = Connect()
    clt = connect.get_config()
    request = connect.connect()
    url = ['http://pic33.photophoto.cn/20141221/0017030088228544_b.jpg','http://pic33.photophoto.cn/20141221/0017030088228544_b.jpg']
    ImageScan(urls = url).get_result(request, clt)
    end = time.time()
    print(end - start)
