# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/8/23
# description: 请求参数signature hook还原

"""

"""
import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

js_code = """
Java.perform(
    function(){

    var DD = Java.use("com.iCitySuzhou.suzhou001.d.d")
    DD.a.overload("a.u$a").implementation = function(p){
        return this.a(p)
    }
     
    var parms = "IMEI867686021254857-IMSI460NNNNNNNNNNNN&&1693302361&&f1190aca-d08e-4041-8666-29931cd89dde"

    var AA = Java.use("com.hualong.framework.b.a")
    /* 测试每行都打印   76c10f5e47f2ad3141d61ce8f65f9bea*/ 
    var str = Java.use("java.lang.String").$new(parms)
    var stringBuffer = Java.use("java.lang.StringBuffer").$new()   //   新建一个对象写法
    var Integer = Java.use("java.lang.Integer")
    var instance = Java.use("java.security.MessageDigest").getInstance("MD5");
    instance.update(str.getBytes());
    var digest = instance.digest()
    var len = digest.length
    for (var i=0;i<len;++i){
        stringBuffer.append(Integer.toString((digest[i] >>> 4) & 15, 16)).append(Integer.toString(digest[i] & 15, 16));
    }
    console.log(stringBuffer.toString())
    }
)
"""
#启动方式1
process = frida.get_usb_device(-1).attach("引力播")
script = process.create_script(js_code)
script.on('message', on_message)
script.load()
sys.stdin.read()  # 保持程序不关闭


