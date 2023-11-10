# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/11/7
# description: 
import os
import sys

import hashlib

"""  m3u8 解析一般流程
1. 首先抓包获取.m3u8的链接下载文件：其中除了版本信息还可能保存着加密字段，eg:21题AES
2. 获取其他加密值，例如21的 Key
2. 21题获取指定片段的解密
     - 获取key: 读文件解密 with open("enc.key") as f： f.read().hex()
     - 获取解密的文件CMD操作   ：openssl aes-128-cbc -d -in segment-0.ts -out desc-0.ts -nosalt -iv 76E4CF6C3E609CD8EAE3B0D2860DC342 -K d2e2b7e68bc120e3929bf54d89448e5e
     - 获取文件的md5【CMD操作】：certutil -hashfile desc-0.ts MD5
"""


# 获取文件的md5-代码操作
def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

# 使用方法
file_path = r'C:\Users\wwj\Downloads\desc-0.ts'
md5_hash = calculate_md5(file_path)
print(f'The MD5 hash of the file is: {md5_hash}')