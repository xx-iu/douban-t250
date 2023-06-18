# -*- coding = utf-8 -*-
# @Time : 2022/1/27 21:01
# @Author : xuxiang
# @File : testurllib.py

import urllib.request
'''
# get请求
response = urllib.request.urlopen("http://www.baidu.com")
print(response.read().decode('utf-8'))
'''
# # post请求
# import urllib.parse
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response = urllib.request.urlopen("http://httpbin.org/post",data =data)
# print(response.read().decode('utf-8'))

response = urllib.request.urlopen("http://www.baidu.com",timeout=1)
print(response.getheader('Date'))