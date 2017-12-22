#! /usr/bin/env python
# -*- coding utf-8 -*-

"""
@author:Xiuzhu
@file:face_detect_facep.py
@time:2017/12/1 11:03
"""


import requests
from json import JSONDecoder

http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = "******************"
secret = "******************"
filepath = r"D:\pycharm\face_detect\picture\1.jpg"

#上传本地文件
data = {"api_key": key, "api_secret": secret, "return_landmark": "1"}
files = {"image_file": open(filepath, "rb")}
response = requests.post(http_url, data=data, files=files)
print(response.text)
# req_con = response.content.decode('utf-8')
# req_dict = JSONDecoder().decode(req_con)
#
# print(req_dict)

#上传url图片
#不要加header
picture = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1512035373340&di=c40e8a2c32f63573c80190f6f86dec0b&imgtype=0&src=http%3A%2F%2Fwww.71lady.net%2Fd%2Ffile%2Fyule%2Fneidiyule%2Fneidizixun%2F2016-01-15%2F198c7a3f1d7b8545fb7ef6a8657dce80.png"
data1 = {'api_key' : key,
           'api_secret' : secret,
           'image_url' : picture,
            "return_landmark":1
        }
response = requests.post(http_url, data=data1)
print(response.text)