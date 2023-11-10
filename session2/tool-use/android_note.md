### 1.基础类
- Context: 上下文 
- PackageManager: 获取安卓系统信息和APP的信息  https://www.cnblogs.com/travellife/p/3932823.html
- Signature：签名 https://developer.android.google.cn/reference/android/content/pm/Signature


### 2.  知识点
- APP代码结构
```html
 业务模块：
 系统模块：com.android.
 第三方模块：网络请求（okhttp），支付(pay)，推送(umeng)等等
```
- APP简单启动顺序
```html
点击APP启动--->执行Application(attach, onCreate方法)------>执行开屏界面Activity--
执行Main Activity(onCreate方法)---->启动成功
``` 
- 常见的类
```html

Context:           上下文 
PackageManager:    获取安卓系统信息和APP的信息  https://www.cnblogs.com/travellife/p/3932823.html
Signature：        签名 https://developer.android.google.cn/reference/android/content/pm/Signature
                   签名关键字&特征值：context.getPackageManager().getPackageInfo(context.getPackageName(), 64).signatures[0].hashCode()
                   
                   
                   
java.lang.Class:   使用这个类可以获取到一个java类下所有的方法   demo: 8-response-enc-frida.py 



  
```

- 反射调用：demochecksum 
```textmate
public static Object a(Object obj, String str, Object obj2, Class cls, Object obj3, Class cls2) {
    try {
        return obj.getClass().getMethod(str, cls, cls2).invoke(obj, obj2, obj3);
    } catch (Exception e) {
        return null;
    }
}
// obj.getClass().getMethod(str, cls, cls2).invoke(obj, obj2, obj3); 
1. obj.getClass()：这个方法返回对象 obj 的运行时类的 Class 对象。通过 getClass() 方法，我们可以获取到对象的类信息。
2. .getMethod(str, cls, cls2)：这个方法用于获取指定方法名和参数类型的方法对象。在这里，str 是方法的名称，cls 和 cls2 是方法的参数类型。通过调用 getMethod() 方法，我们可以获取到指定方法的 Method 对象。
3. .invoke(obj, obj2, obj3)：这个方法用于调用指定对象的方法。在这里，obj 是要调用方法的对象，obj2 和 obj3 是方法的参数。通过调用 invoke() 方法，我们可以执行指定对象的指定方法，并传递相应的参数。

```
- 动态加载dex: classloader  Demo：8-response-classloader切换-ASE-.py

