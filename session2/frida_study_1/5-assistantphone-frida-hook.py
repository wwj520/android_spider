# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/8/30
# description: 
import frida,sys

def on_message(message, data):
    if message['type'] == 'send':
        print("1[*] {0}".format(message['payload']))
    else:
        print(message)

js_code = """
Java.perform(
    function(){
        console.log("start")
        var  LoginQueryObj = Java.use("com.bytedance.sdk.account.mobile.query.LoginQueryObj")
        LoginQueryObj.$init.overload('java.lang.String', 'java.lang.String', 'java.lang.String').implementation = function(str,str2,str3){
            console.log('mMobile:', str);
            
            // 
            this.$init(str, str2, str3);
            
        }
     
        var Utils = Java.use("com.bytedance.common.utility.StringUtils")
        var str = Java.use("java.lang.String")   
        var str1 = Java.use("java.lang.String").$new("WUwenjie521")
        
        // 如果方法是静态的可以直接调
        var encrypt_pwd = Utils.encryptWithXor("WUwenjie521")
        console.log("encrypt_pwd:" + encrypt_pwd)
        
       Utils.encryptWithXor.implementation  = function(str_){
            console.log(str_+"|" + this.encryptWithXor(str_))
    }
    
     
    // 日志   
    function printstack() {
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
        }    
        
    
    }
)
"""







#启动方式1
process = frida.get_usb_device(-1).attach("PICO VR")
script = process.create_script(js_code)
script.on('message', on_message)
script.load()
sys.stdin.read()  # 保持程序不关闭

