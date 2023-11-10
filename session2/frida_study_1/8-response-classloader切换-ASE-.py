# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/9/7
# description:

"""  **************** 场景 ****************
-  jadx中有代码，但Hook不到类
-  可能是动态加载dex，类可能在另外的classloader中，需要切换 classloader 再hook
-  https://www.jianshu.com/p/96a72d1a7974
"""


import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


hook_class = """
Java.perform(function(){

    var MAppliction = Java.use('com.xbiao.MAppliction')
    
    console.log(MAppliction.getInstance(). getResources().getString(2131820921))
    
    // 1. 枚举Java虚拟机中的所有类加载器
    Java.enumerateClassLoaders({
        
        // 2. onMatch：这是一个回调函数，每当找到一个类加载器【时】，都会调用这个函数。这个函数的参数是当前找到的类加载器
        onMatch: function(loader){
            
            //2.1 Java.classFactory.loader = loader;这行代码是在设置当前的类加载器为loader。这样，后续使用Java.use等方法加载类时，就会使用这个类加载器
            Java.classFactory.loader = loader;
            var TestClass;
            try{
                TestClass = Java.use("com.xbiao.utils.AESedeUtil");
                TestClass.decrypt.implementation = function(p1, p2){
                    console.log('参数 1:'+p1)
                    console.log('参数 2:'+p2)
                    var rest = this.decrypt(p1,p2)
                    console.log("加密结果："+ rest)
                    return rest
                }
            }catch(error){
                if (error.message.includes("ClassNotFoundException")){
                    console.log(loader)
                    console.log(" You are trying to load encrypted class, trying next loader");
                
                }else{
                        console.log(error.message);
                    }
            }
        },
        
        // 3. onComplete：这是一个回调函数，当枚举类加载器的操作完成【后】，会调用这个函数。这个函数没有参数。
        // 可以在这个函数中执行一些清理操作或者其他需要在枚举完成后执行的操作。    
        onComplete: function(){
        }

    })
    
})
"""


process = frida.get_usb_device(-1).attach("腕表之家")
# script = process.create_script(hook_class)
script = process.create_script(hook_class)
script.on('message', on_message)
script.load()
sys.stdin.read()  # 保持程序不关闭

