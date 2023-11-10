# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/11/7
# description: 
import os
import sys
import execjs
import json
import requests


""" 当没法在jadx中搜索到任何数据时，可以通过获取当前的 Activity
    code:  adb shell "dumpsys window | grep mCurrentFocus" // 查看当前运行的activity  可能需要先adb进入su
"""



headers = {
    'Host': 'www.python-spider.com',
    'content-type': 'application/json',
    'content-length': '70',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.9.1',
}
with open("./js_files/10.js")as f:
    compile = execjs.compile(f.read())

page_list = [i for i in range(1, 101)]
sum_num = 0
while page_list:
    for i in page_list:
        rest = compile.call("get_sign", i)
        times = int(rest.split("-")[0])
        signs = rest.split("-")[1]
        data = {"page": i, "t": times, "sign": signs}
        response = requests.post('https://www.python-spider.com/api/app10', headers=headers, data=json.dumps(data))
        res = response.json()

        if res["status"] == "1":
            page_list.remove(i)
            for row in res["data"]:
                sum_num += int(row['value'].strip('\r'))
        else:
            print(f"page={i}, 程序异常")

print(sum_num)