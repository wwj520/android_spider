# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/8/23
# description:  Hook-简单签名校验、com.chaozhuo.texteditor.apk

"""
一、frida签名
1 签名关键字&特征值
    固定写法： context.getPackageManager().getPackageInfo(context.getPackageName(), 64).signatures[0].hashCode()

二、 案例流程
    1. 为hook签名流程重新打包apk
    2. hook: Signature....hashCod
    3. js代码
    3.1 hook阶段：

    4.0 可以用 AndroidKiller直接去修改指定位置的smail代码，再进行编译


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
         console.log('i am coming')
         var Signature = Java.use("android.content.pm.Signature") // 从文档中获取到的固定路径
         Signature.hashCode.implementation = function(){
            console.log("hashCode")
            return this.hashCode()
         }
         
         Signature.toByteArray.implementation = function() {
            console.log('toByteArray')
            printstack()
            return this.toByteArray()
        }
        
         // 日志打印看在哪步有问题---固定日志写法
         function printstack() {
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
        }
         
         var aa = Java.use("com.chaozhuo.texteditor.widget.a")
         // overload: 重载 此处的用法是为了避免取了同名的a方法，指定加载Context类型的a方法
         aa.a.overload("android.content.Context").implementation = function(){
            return true
         }       
    }

)
"""

#启动方式2：这种方式需要关闭在手机关掉Magisk Hide，路径(Magisk软件的Magisk Manager > Settings >Magisk > Magisk Hide)
device = frida.get_usb_device(-1)
print(device)
pid = device.spawn(['com.xbiao'])
print(pid)
process = device.attach(pid)

script = process.create_script(js_code)
script.on('message', on_message)
print('[*] Running')
script.load()

device.resume(pid)
sys.stdin.read()




