## Android如何集成本地模块
####  步骤：
    1. 将 ..\session6\tools\ratel-extension 放入项目中与app同级的目录下
    2. 在setting.gradle 中添加 【include ':ratel-extension'】，并同步设置
    3. build.gradle中添加依赖， 并更新设置
        dependencies { 
            ...
            implementation project(path:":ratel-extension")
        }
#### 集成之后如何启动一个 Sekiro服务
    地址： ..ratel01\app\src\main\java\com\example\ratel01\AppiumEntry.java
    code:
            package com.example.ratel01;
            import android.os.Build;
            import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
            import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
            import ratel.com.yuanrenxue.extension.superappium.sekiro.SekiroStarter;
            
            public class AppiumEntry implements IRposedHookLoadPackage {
                private final String CLIEND_ID = Build.BRAND + Build.MODEL.replace(" ", "")+Build.HOST;
            
                @Override
                public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
                    // SekiroStarter 要引用本地的
                    SekiroStarter.startService("192.168.34.202", 5612, CLIEND_ID);
                }
}

## SekiroDump相关API 的使⽤----直接读 ratel-extension 源码
```text
  public void onSekiroRequest(SekiroRequest sekiroRequest, HandlerRegistry handlerRegistry) {
        handlerRegistry.registerSekiroHandler(new DumpTopActivityHandler());
        handlerRegistry.registerSekiroHandler(new DumpTopFragmentHandler());
        handlerRegistry.registerSekiroHandler(new ExecuteJsOnWebViewHandler());
        handlerRegistry.registerSekiroHandler(new FileExploreHandler());
        handlerRegistry.registerSekiroHandler(new ScreenShotHandler());



```

    
