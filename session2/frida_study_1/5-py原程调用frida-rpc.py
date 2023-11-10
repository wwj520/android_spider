# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/8/31
# description:  py 调用frida-rpc固定写法
from urllib.parse import quote_plus
print(quote_plus("/"))
import frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

rpc_code = """
rpc.exports = {
     //PS: 函数名不要大写；函数名是py要调用的
     get: function(str_){
        var enc = ''
        Java.perform(function () {
            var Utils = Java.use("com.bytedance.common.utility.StringUtils")
            enc = Utils.encryptWithXor(str_)
         }) ;
     // 注意return的位置    
     return enc
     }
}
"""

def run():
    process = frida.get_usb_device(-1).attach("PICO VR")
    script = process.create_script(rpc_code)
    script.on('message', on_message)
    script.load()
    # 获取rpc的值，script.exports会将代码注入到安卓代码中
    # get 是方法名
    result = script.exports.get("WUwenjie521")
    return result


if __name__ == '__main__':
    r = run()
    print(r)