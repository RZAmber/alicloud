#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import time
import random
import binascii
from hashlib import sha1
import hmac
import base64

appid = '1255551197'
secret_id = '******************'
secret_key = '******************'
bucket = 'facedetect'

currentTime = int(time.time())
expiredTime = currentTime + 2592000
rand = random.randint(1,9999999999)
picture = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1508146217268&di=f81fdcd1d14a66281d1c202db9b3fe88&imgtype=0&src=http%3A%2F%2Fcms-bucket.nosdn.127.net%2Fcatchpic%2F3%2F3b%2F3b3314b76d844c47c191dc6245228143.jpg%3FimageView%26thumbnail%3D550x0'

##测试人脸检测api

#拼接签名串
original = "a=%s&b=%s&k=%s&e=%d&t=%d&r=%d&u=%s&f="%(appid,bucket,secret_id,expiredTime,currentTime,rand,'0')

#生成Authorization签名字段
secret_key1 = secret_key.encode(encoding='utf-8')
original1 = original.encode(encoding='utf-8')
hashed = hmac.new(secret_key1, original1, sha1)
Authorization = base64.b64encode(hashed.digest() + original1).rstrip()

#request api
headers = {'content-type':'application/json', "Host":"service.image.myqcloud.com", "Authorization":Authorization}
data = {'appid' : appid,
           'mode' : 1,
           'url' : picture
        }
url = 'http://service.image.myqcloud.com/face/detect'
req = requests.post(url, data = json.dumps(data), headers = headers)
print(req.text)

'''
import os
from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers
#调用sdk
client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)
url = 'http://service.image.myqcloud.com/face/detect'
# 人脸检测
# 单个图片Url, mode:1为检测最大的人脸 , 0为检测所有人脸
print(client.face_detect(CIUrl('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1508146217268&di=f81fdcd1d14a66281d1c202db9b3fe88&imgtype=0&src=http%3A%2F%2Fcms-bucket.nosdn.127.net%2Fcatchpic%2F3%2F3b%2F3b3314b76d844c47c191dc6245228143.jpg%3FimageView%26thumbnail%3D550x0')))
# 单个图片file,mode:1为检测最大的人脸 , 0为检测所有人脸
#print(client.face_detect(CIFile('./hot2.jpg')))
'''