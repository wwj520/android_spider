# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/9/7
# description:  如何写一个frida程序，hook某一类的所有方法
# url : https://tool.oschina.net/apidocs/apidoc?api=jdk-zh
"""了解 Java & 安卓 的一些类
         argumentTypes      -----------------------------------  获取参数类型,其有属性className、....
         PackageManager类   -----------------------------------
         java.lang.Class    -----------------------------------  调用class下的方法可以改类下的所有方法....
         overloads          -----------------------------------  获取某个方法的所有重载. eg: functaion_1.overloads
         enumerateClassLoaders    -----------------------------  枚举Java虚拟机中的所有类加载器，通常会跟两个函数：onMatch、onComplete
         getInterfaces ---------------------------------------   // 使用反射获取类实现的接口数组   var targetClass = Java.use(name);
                                                                                                   var interfaceList = targetClass.class.getInterfaces(); // 使用反射获取类实现的接口数组
         java.security.Signature
         Context类
         java.util.HashMap Map SortedMap TreeMap
         javax.crypto.Cipher
         java.security.PublicKey
         android.util.Log        -----------------------------   日志打印
         java.security.MessageDigest
         javax.crypto.Mac
         javax.crypto.spec.SecretKeySpec
         javax.crypto.spec.DESKeySpec
         javax.crypto.spec.IvParameterSpec
         java.security.spec.X509EncodedKeySpec
         java.security.spec.RSAPublicKeySpec
"""


import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


# 1.使用 java.lang.Class固定的写法获取一个类下所有的方法
hook_class = """
Java.perform(function(){
    hookClass("com.xbiao.utils.net.NetContent")
})


function hookClass(className){
    var MyClass = Java.use(className)        
    // 1. 获取类下所有方法名  
    // getDeclaredMethods 是获取类中自己声明的方法，即自己声明的任何权限的方法，包括私有方法
    var methods = MyClass.class.getDeclaredMethods()
    
    // 2. 遍历所有方法，获得方法名 
    methods.forEach(function(method){
        var method_name = method.getName()  // getName获取方法名

        // 3. overloads- 获取该方法的所有重载
        var overloads = MyClass[method_name].overloads
        
        // 4. 遍历所有重载
        overloads.forEach(function(overload){
            // hook 重载
            // argumentTypes：可以获取参数类型
            
            var prot = "("
             for (var i = 0; i < overload.argumentTypes.length; i++) {
                    prot += overload.argumentTypes[i].className + ","
                    }
             prot+=")"
             console.log("方法:"+ method_name, "参数类型:"+prot)
             
             var vMethodName = className + "." + method_name
            
             overload.implementation = function(){
                console.log("******************************************")
                console.log("function:"+ vMethodName)
                for (var i = 0; i < arguments.length; i++) {
                    console.log("agrument:"+ JSON.stringify(arguments[i]))
                    }
                //5. 返回原方法的调用（hook重载），注意要return 回原本的请求
                var res = this[method_name].apply(this, arguments)
                console.log("function:"+ vMethodName, "result:"+ JSON.stringify(res))
                return res
            }
        })
    })       
}
"""


process = frida.get_usb_device(-1).attach("腕表之家")
# script = process.create_script(hook_class)
script = process.create_script(hook_class)
script.on('message', on_message)
script.load()
sys.stdin.read()  # 保持程序不关闭

