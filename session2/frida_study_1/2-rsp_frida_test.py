# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/8/23
# description: 

"""frida 基本使用
1.import frida, sys
2. 固定的 on_message方法
3. 写固定格式的js
    Java.perform(
    function(){
        console.log('i am coming')
        var MainActivity = Java.use('xxxxx.MainActivity')
        MainActivity.要hook的方法名.implementation = function(参数){
            this.方法(参数) // 返回原始的方法
            console.log()
            console.log()
        }
    }
)

4. 启动方式1： app 已经启动
    # 获取包名： ps -A | grep xxx 两者在终端 frida-ps -U 获取
    process = frida.get_usb_device(-1).attach("包名")
    script = process.create_script(test)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()
"""


import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


test = '''
Java.perform(
    function(){
        console.log('i am coming')
        var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity')
        MainActivity.onClick.implementation = function(v){
            this.onClick(v)
            console.log('mmm:'+this.m.value)
            console.log('nnn:'+this.n.value)
        }
        
        // 匿名函数-run hook
        var TT = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity$1')
        TT.run.implementation = function(){
            this.this$0.value.m.value = 1
            this.this$0.value.n.value = 2
            this.run()
        }
    }
)
'''


"""
获取手机进程名：ps -A | grep xxx
"""

#启动方式1
# 这里面直接attach("com.example.seccon2015.rock_paper_scissors") 可能会报错，rock_paper_scissors是从frida-ps -U这获取的
process = frida.get_usb_device(-1).attach("rock_paper_scissors")
script = process.create_script(test)
script.on('message', on_message)
script.load()
sys.stdin.read()  # 保持程序不关闭

#启动方式2：这种方式需要关闭在手机关掉Magisk Hide，路径(Magisk软件的Magisk Manager > Settings >Magisk > Magisk Hide)
# device = frida.get_usb_device(-1)
# pid = device.spawn(['com.example.seccon2015.rock_paper_scissors'])
# process = device.attach(pid)
#
script = process.create_script(test)
# script.on('message', on_message)
# print('[*] Running')
# script.load()
#
# device.resume(pid)
# sys.stdin.read()



