### Frida 安装
- 手机端：Frida-server https://github.com/frida/frida/releases 
     adb push  adb push frida-server /data/local/tmp/
     adb shell
     su
     cd /data/local/tmp
     修改权限： chmod 777 frida-server
     启动server: ./frida-server&
    
- PC: pip安装对应版本的 frida、frida-tools

- 测试安装：
    frida-ps -U 电脑上运行 android.process.acore 字样表示成功
- 端口转发
     adb forward tcp:27043 tcp:27043
     adb forward tcp:27042 tcp:27042

   
### Frida API介绍 : https://frida.re/docs/javascript-api/
#### 语法介绍
- 0 常用模块API
```html
Java模块：       Hook Java 层的类 方法 相关
Process模块：    处理当前线程相关
Interceptor模块：操作指针相关，多用来Hook Native 相关
Memory模块：     内存操作相关
Module模块：     处理so相关
```
- 1 Hook 基本框架>>>>> demo1:hook猜拳游戏rsp
        {
          apk：rps-frida-test.apk
          hook程序： rsp_frida_test.py
        }
        
- 2  frida Hook Java类Tips
    ``` html
     访问成员变量写法：    this.成员变量名.value
     
     从匿名类/内部类访问外部类的属性写法：this.this$0.value.外部类的属性名.value
     新建一个对象写法 new:   类.方法名.$new(参数) eg：新建一个StringBuffer--- Java.use("java.lang.StringBuffer").$new()
     重载写法:               类.方法名.overload(参数1，参数2.......).implementation
     hook 构造方法:          类.$init().implementation----- eg:assistantphone-frida-hook.py中有案例
     hook 内部类：           类.$内部类名：  eg     var InnerClass = Java.use("com.xiaojianbang.app.Money$innerClass");
                                                    // 重写内部类的 $init 方法
                                                    InnerClass.$init.overload("java.lang.String","int").implementation
     hook 匿名类写法：   function main(){
                                Java.perform(function(){
                                    // hook 匿名类
                                    // 匿名类在 smail中以 $1, $2 等方式存在, 需要通过 java 行号去 smail 找到准确的匿名类名称 
                                    var NiMingClass = Java.use("com.xiaojianbang.app.MainActivity$1");
                                    NiMingClass.getInfo.implementation = function (){
                                        return "kevin change 匿名类";
                                    }
                                })
                            }    
     
     
    ```
- 2.1 命令使用
```text
- attach 启动

         frida -U com.kevin.android -l hook.js
         frida -UF -l hook.js // 运行当前打开的应用
         
-  spawn 启动

         frida -U -f com.kevin.android -l demo1.js
         
```
 
- 3 类型转换    
    
- 5 frida rpc：远程主动调用安卓代码 --- demo:5-py原程调用frida-rpc.py
```javascript
rpc.exports = {
     get: function(str_){  //PS: 函数名不要大写；函数名是py要调用的
        var enc = ''       // enc要做全局
        Java.perform(function () {
            var Utils = Java.use("com.bytedance.common.utility.StringUtils")
            enc = Utils.encryptWithXor(str_)
         }) ;
     // 注意return的位置    
     return enc
     }
}
```
- 6 hook so文件基本写法
 ```javascript
Java.perform(function(){
    var 变量 = Module.getExportByName("so文件名", "在so文件中的文件开头 - EXPORT后面的值")
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

```

### 固定写法
- 日志打印
```javascript
 function printstack() {
    console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
}
```
-  字节数组转hex字符串
```javascript
 var ByteString = Java.use('com.android.okhttp.okio.ByteString')
 result = ByteString.of(byte_data).hex()
```

### c 基本使⽤
- 安装：pip install objection
























### 问题解决
- 还原关于打印[object object] 
```text
解决：前提确定是可打印的  
     方法一：
         1.先确认object是什么类型(比如要打印p) 先console.log(p.$className) 查看p是什么数据类型
         2.Java.cast 把p强转为对应类型
         3.调用该类对应的输出方法。通常有一个toString()方法
         --- eg:
             var Map = Java.use('java.util.Map')
             var NewP = Java.cast(P, Map)
             把P 转成 Map类型

     方法二：   
         使用js里的JSON类尝试 console.log(JSON.stringify(p))可能打印不出来字符串，一般能打印出p的字节数组。（可以用着你的数据和真实数据的对比）

```
  