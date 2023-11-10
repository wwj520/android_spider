# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/9/9
# description: hook so文件
""" so文件hook基本语法

Java.perform(function(){
    var 变量 = Module.getExportByName("so文件名", "函数名：在so文件中的文件开头 - EXPORT后面的值，ida打开能看到")
    Interceptor.attach(变量, {

        // hook 开始需要操作的函数
        onEnter：function(args){
            *******
        },
        // hook 结束操作的方法
        onLeave: function(retval){
        }
    })
})
"""

import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


js_code = """
Java.perform(function(){
    var ByteString = Java.use('com.android.okhttp.okio.ByteString')

    var Native = Java.use("com.shjt.map.tool.Native");
    Native.decode2.implementation = function(byte_data){
        console.log("str: " + Java.use("java.lang.String").$new(byte_data))
        console.log("hex: ", ByteString.of(byte_data).hex())
        console.log("array: " + JSON.stringify(byte_data))
        return this.decode2(byte_data)
    }
    
    // 两个so文件hook有时候需要猜测哪个是 k 、iv
    // hook aes_decrypt_cbc
    var aes_decrypt_cbc = Module.getExportByName("libnative.so", "_Z15aes_decrypt_cbcPKhjPhPKjiS0_")
    Interceptor.attach(aes_decrypt_cbc, {
        onEnter: function(args){
            console.log("*************hook: aes_decrypt_cbc*************")
            console.log("参数1",args[0].readByteArray(16))
            console.log("参数2",args[1].toInt32())
            console.log("参数3",args[2].readByteArray(16))
            console.log("参数4",args[3].readByteArray(16))
            console.log("参数5",args[4].toInt32())
            console.log("参数6",args[5].readByteArray(16))
  
        },
        onLeave: function(retval){
        }
    })
    

    // hook  aes_key_setup方法
    var aes_key_setup = Module.getExportByName("libnative.so", "_Z13aes_key_setupPKhPji")
    Interceptor.attach(aes_key_setup, {
        onEnter: function(args){
            console.log("*************hook:aes_key_setup*************")
            
            // 这里用readByteArray是应该AES加密的k,iv都是16位字节类型，
            console.log("参数1",args[0].readByteArray(16))
            console.log("参数2",args[1].readByteArray(16))
            console.log("参数3",args[2].toInt32())
  
        },
        onLeave: function(retval){
        
        }
    })
    
    // hook 请求参数
    Module.getExportByName("libnative.so", )
     
    
    
    
})

"""
process = frida.get_usb_device(-1).attach("上海公交")
script = process.create_script(js_code)
script.on('message', on_message)
script.load()
sys.stdin.read()  # 保持程序不关闭


