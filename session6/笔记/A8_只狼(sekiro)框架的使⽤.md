## sekiro 安装部署
```text

1. 官方文档：https://sekiro.iinti.cn/sekiro-doc/
2.  window版本下载： https://oss.iinti.cn/sekiro/sekiro-demo，下载完成后直接启动sekiro.bat文件
3. 测试链接
    http://127.0.0.1:5612/business-demo/groupList
    http://127.0.0.1:5612/business-demo/clientQueue?group=test
    http://127.0.0.1:5612/business-demo/invoke?group=demo&action=clienTime
```
## Demo1: 写一个Sekiro服务实例步骤
1. 添加配置：demo..\MysterBox\app\build.gradle
    ```text
       在build.gradle中添加
            dependencies {
                **
                implementation 'cn.iinti.sekiro3.business:sekiro-business-api:1.1'
            }
       在 settings.gradle 添加maven仓库 
            repositories{
                **
                maven { url "https://nexus.iinti.cn/repository/maven-public/" } 
            }
    ```
2. 在清单文件中添加【网络权限】 
        
         <uses-permission android:name="android.permission.INTERNET"/>
         
3. 在..app\src\androidTest\java 中添加handlers文件夹，用于存储 handler 通道脚本

4. 写一个Sekiro服务实例：
    ```text
        ############ 客户端 ############ \MysterBox\app\src\main\java\com\example\mysterbox\MainActivity.java
        // 1. 创建SekiroClient客户端： group_name、clientId 需自定义
        SekiroClient sekiroClient = new SekiroClient("group_name", clientId, "192.168.34.202", 5612);
     
        // 2. 注册服务
        // 2.1 ClientTimeHandler 是handler中的类
        sekiroClient.setupSekiroRequestInitializer(new SekiroRequestInitializer() {
            @Override
            public void onSekiroRequest(SekiroRequest sekiroRequest, HandlerRegistry handlerRegistry) {
                handlerRegistry.registerSekiroHandler(new ClientTimeHandler());
            }
        });
        // 3 启动服务
        sekiroClient.start()
     
        ############ 服务端 ####【在handler是程序包中】######## ..\MysterBox\app\src\main\java\com\example\mysterbox\handlers\ClientTimeHandler.java
         
        // Action是一个注解（Annotation），在路由中体现: //business-demo/invoke?group=group_name&page=10&action=clienTime
        @Action("clienTime")  // Action是一个注解（Annotation）
        public class ClientTimeHandler implements RequestHandler {
           @    
            
            @Override
            public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
                sekiroResponse.success("当前时间" + System.currentTimeMillis());
        
            }
        }
 
    ```
1. 添加配置：demo..\MysterBox\app\build.gradle
    ```text
       在build.gradle中添加
            dependencies {
                **
                implementation 'cn.iinti.sekiro3.business:sekiro-business-api:1.1'
            }
       在 settings.gradle 添加maven仓库 
            repositories{
                **
                maven { url "https://nexus.iinti.cn/repository/maven-public/" } 
            }
    ```
2. 在清单文件中添加【网络权限】 
        
         <uses-permission android:name="android.permission.INTERNET"/>
         
3. 在..app\src\androidTest\java 中添加handlers文件夹，用于存储 handler 通道脚本

4. 写一个Sekiro服务实例
    ```text
        ############ 客户端 ############ \MysterBox\app\src\main\java\com\example\mysterbox\MainActivity.java
        // 1. 创建SekiroClient客户端： group_name、clientId 需自定义
        SekiroClient sekiroClient = new SekiroClient("group_name", clientId, "192.168.34.202", 5612);
     
        // 2. 注册服务C
        // 2.1 ClientTimeHandler 是handler中的类
        sekiroClient.setupSekiroRequestInitializer(new SekiroRequestInitializer() {
            @Override
            public void onSekiroRequest(SekiroRequest sekiroRequest, HandlerRegistry handlerRegistry) {
                handlerRegistry.registerSekiroHandler(new ClientTimeHandler());
            }
        });
        // 3 启动服务
        sekiroClient.start()
     
        ############ 服务端 ############ ..\MysterBox\app\src\main\java\com\example\mysterbox\handlers\ClientTimeHandler.java
         
        // Action是一个注解（Annotation），在路由中体现: //business-demo/invoke?group=group_name&page=10&action=clienTime
        @Action("clienTime")  // Action是一个注解（Annotation）
        public class ClientTimeHandler implements RequestHandler {
           @    
            
            @Override
            public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
                sekiroResponse.success("当前时间" + System.currentTimeMillis());
        
            }
        }
 
    ```
## Demo2: Sekrio + 平头哥主动调用结合
    实例：
        D:\AndroidStudioProjects\ratel01\app\src\main\java\com\example\ratel01\handlers\SignHandler.java
        D:\AndroidStudioProjects\ratel01\app\src\main\java\com\example\ratel01\SekiroEntry.java
        D:\AndroidStudioProjects\MysterBox\app\src\main\java\com\example\mysterbox\Sign.java
- 注意
     
      在平头哥插件中同样需要添加Sekiro配置和网络权限
-  SekiroEntry.java
```text
package com.example.ratel01;

import android.os.Build;
import android.util.Log;

import com.example.ratel01.handlers.SignHandler;
import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

import cn.iinti.sekiro3.business.api.SekiroClient;
import cn.iinti.sekiro3.business.api.interfaze.HandlerRegistry;
import cn.iinti.sekiro3.business.api.interfaze.SekiroRequest;
import cn.iinti.sekiro3.business.api.interfaze.SekiroRequestInitializer;

public class SekiroEntry implements IRposedHookLoadPackage {
    private static final String TAG = "yuanrenxue---";
    private final String CLIEND_ID = Build.BRAND + Build.MODEL.replace(" ", "")+Build.HOST;

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.example.mysterbox")) {
            Log.d(TAG, "handleLoadPackage: hook sign success");

            SekiroClient sekiroClient = new SekiroClient("signGroup", CLIEND_ID, "192.168.34.202", 5612);
            // 1.2  注册服务
            sekiroClient.setupSekiroRequestInitializer(new SekiroRequestInitializer() {
                @Override
                public void onSekiroRequest(SekiroRequest sekiroRequest, HandlerRegistry handlerRegistry) {
                    handlerRegistry.registerSekiroHandler(new SignHandler(lpparam.classLoader));
                }
            });
            // 1.3 启动服务
            sekiroClient.start();

        }
    }
}
```    
      
            
- SignHandler.java
```text
package com.example.ratel01.handlers;

import android.util.Log;

import com.virjar.ratel.api.rposed.RposedHelpers;

import cn.iinti.sekiro3.business.api.interfaze.Action;
import cn.iinti.sekiro3.business.api.interfaze.AutoBind; //这里不能引入 import com.virjar.sekiro.api.databind.AutoBind;
import cn.iinti.sekiro3.business.api.interfaze.RequestHandler;
import cn.iinti.sekiro3.business.api.interfaze.SekiroRequest;
import cn.iinti.sekiro3.business.api.interfaze.SekiroResponse;

@Action("getSign")
public class SignHandler implements RequestHandler {
    private static final String TAG = "yuanrenxue--";
    @AutoBind
    private Integer page;

    private final ClassLoader mClassLoader;

    // 这里这这样写是为了 从hook程序(SekiroEntry.java)中接收 classLoader
    public SignHandler(ClassLoader classLoader) {
        mClassLoader = classLoader;
    }

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
        Log.d(TAG, "handleRequest: " + this.page);
        Class<?> loadClass = RposedHelpers.findClass("com.example.mysterbox.Sign", this.mClassLoader);
        String sign = (String) RposedHelpers.callStaticMethod(loadClass, "getSign", this.page);
        sekiroResponse.success(sign);
    }
    /* 代码补充：rpc被线程检测的问题
    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
        Log.d(TAG, "handleRequest: " + page);
        Class<?> loadClass = RposedHelpers.findClass("com.example.mysterbox.Sign", this.mClassLoader);
        // new Handler 这里这样写的原因是要丢到主线程中调用,RPC默认是子线程中
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @Override
            public void run() {
                String sign = (String) RposedHelpers.callStaticMethod(loadClass, "getSign", page);
                sekiroResponse.success(sign);
            }
        });
    }
    */
    
    
}
```

- Sign.java
```text
package com.example.mysterbox;

import java.math.BigInteger;
import java.security.MessageDigest;

public class Sign {
    public  static String getSign(Integer page) throws  Exception{
        return new BigInteger(MessageDigest.getInstance("MD5").digest((page + "").getBytes())).toString(16);
    }
}



```

    
