# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/9/12
# description: 利用proto.exe
import binascii
import base64
import urllib.parse

import blackboxprotobuf
import requests
from Crypto.Util.Padding import pad, unpad  # 补齐，去补齐
from Crypto.Cipher import AES


def format_request_parms():
    """组合request参数"""
    with open(r"D:\all_python_study\yuanrenxue_android_code\session2\frida_study_1\frida_10_protobuf_hook_so\final_request_proto.bin", 'rb') as f:
        data = f.read()
    messgae, message_type =blackboxprotobuf.protobuf_to_json(data, message_type=None)
    data_dict = blackboxprotobuf.decode_message(data)[0]
    data_dict['1']['2']['2'] = bytes("1128路", encoding="utf-8")
    request_data = blackboxprotobuf.encode_message(data_dict, message_type=message_type)
    request_data = aes_encry(request_data)
    request_data = base64.b64encode(request_data)
    print(request_data)
    return request_data


def aes_encry(ori):
    key = '2fd3028e14a45d1f8b6eb0b2adb7caaf'
    iv = '754c8fd584facf6210376b2b72b063e4'
    # binascii.a2b_hex：返回由十六进制字符串十六进制表示的二进制数据
    aes = AES.new(binascii.a2b_hex(key), AES.MODE_CBC, binascii.a2b_hex(iv))
    return aes.encrypt(pad(ori, 16))


def aes_decry(ori):
    key = '2fd3028e14a45d1f8b6eb0b2adb7caaf'
    iv = '754c8fd584facf6210376b2b72b063e4'
    aes = AES.new(binascii.a2b_hex(key), AES.MODE_CBC, binascii.a2b_hex(iv))
    return unpad(aes.decrypt(ori), 16)


def req(url, data):
    header = {
        'Accept': 'application/json,application/xml,application/xhtml+xml,text/html;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; Nexus 6P Build/MDA89D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Host': 'lbs.jt.sh.cn:8082'
    }
    r = requests.post(url=url, data=data, headers=header)
    return r.content


def main():
    request_data = format_request_parms()
    # 抓取
    postdata = 'request=' + urllib.parse.quote(request_data.decode(), safe='') + '%0A'
    print(postdata)
    res_data = req('http://lbs.jt.sh.cn:8082/app/rls/monitor', postdata)
    decry_data = aes_decry(res_data)
    json_data, type_data = blackboxprotobuf.protobuf_to_json(decry_data, message_type=None)
    print(json_data)


if __name__ == '__main__':
    main()