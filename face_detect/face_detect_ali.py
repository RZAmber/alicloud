#! /usr/bin/env python
# -*- coding utf-8 -*-

"""
@author:Xiuzhu
@file:face_detect_ali.py
@time:2017/11/30 8:34
"""

import urllib
import datetime
import base64
import hmac
import hashlib
import json
import requests

def get_current_date():
    date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
    return date
def to_md5_base64(strBody):
    hash = hashlib.md5()
    hash.update(strBody.encode('utf-8'))
    return base64.b64encode(hash.digest()).strip()
def to_sha1_base64(stringToSign, secret):
    hmacsha1 = hmac.new(secret.encode(encoding='utf-8'), stringToSign.encode(encoding='utf-8'), hashlib.sha1)
    return base64.b64encode(hmacsha1.digest()).rstrip()
ak_id = '*********'
ak_secret = '**********'
options = {
    'url': 'https://dtplus-cn-shanghai.data.aliyuncs.com/face/attribute',
    'method': 'POST',
    'body': json.dumps({"type": 0,
                        "image_url":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1512035373340&di=c40e8a2c32f63573c80190f6f86dec0b&imgtype=0&src=http%3A%2F%2Fwww.71lady.net%2Fd%2Ffile%2Fyule%2Fneidiyule%2Fneidizixun%2F2016-01-15%2F198c7a3f1d7b8545fb7ef6a8657dce80.png"},
                       separators=(',', ':')),
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'date':  get_current_date(),
        'authorization': ''
    }
}

body = ''
if 'body' in options:
    body = options['body']

bodymd5 = ''
if not body == '':
    bodymd5 = to_md5_base64(body)

urlPath = urllib.parse.urlparse(options['url'])
if urlPath.query != '':
    urlPath = urlPath.path + "?" + urlPath.query
else:
    urlPath = urlPath.path
stringToSign = options['method'] + '\n' + options['headers']['accept'] + '\n' + str(bodymd5,encoding = "utf-8") + '\n' + options['headers']['content-type'] + '\n' + options['headers']['date'] + '\n' + urlPath
signature = to_sha1_base64(stringToSign, ak_secret)

authHeader = 'Dataplus ' + ak_id + ':'+ str(signature,encoding="utf-8")
options['headers']['authorization'] = authHeader

request = None
method = options['method']
url = options['url']

if 'GET' == method or 'DELETE' == method:
    request = requests.get(url, data = options['body'],headers = options['headers'])
elif 'POST' == method or 'PUT' == method:
    request = requests.post(url, data = options['body'], headers=options['headers'])

print(request.text)