#! /usr/bin/env python
# -*- coding utf-8 -*-

"""
@author:Xiuzhu
@file:face_detect_baidu.py
@time:2017/11/29 14:17
"""

import requests
import json
from PIL import Image
from io import BytesIO
import base64
import urllib
grant_type = "client_credentials"
client_id = "**********"  #API KEY
client_secret = "*************" # SECRET KEY

url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=%s&client_id=%s&client_secret=%s&"\
       %(grant_type, client_id, client_secret)

headers = {'content-type':'application/json'}
req = requests.post(url, headers = headers)
#服务器返回json文本参数
#将JSON编码的字符串转换为一个Python数据结构
#data = json.loads(json_str)
#获取access token
data = json.loads(req.text)
access_token =data['access_token']
print(access_token)
img = 0
picture = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1508146217268&di=f81fdcd1d14a66281d1c202db9b3fe88&imgtype=0&src=http%3A%2F%2Fcms-bucket.nosdn.127.net%2Fcatchpic%2F3%2F3b%2F3b3314b76d844c47c191dc6245228143.jpg%3FimageView%26thumbnail%3D550x0'
response = requests.get(picture)
image = Image.open(BytesIO(response.content))
image.save('D:/pycharm/face_detect/picture/1.jpg')
#二进制打开图片，转为base64
#加r是防止地址被转义
f = open(r'D:/pycharm/face_detect/picture/1.jpg','rb')
img = base64.b64encode(f.read())
data = {'face_field':"age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities", "image":img, "max_face_num" :5}

request_url = "https://aip.baidubce.com/rest/2.0/face/v2/detect" + "?access_token=" + access_token
header = {'content-type':'application/x-www-form-urlencoded'}

req = requests.post(request_url, data = data, headers = headers)
print(req.text)

