### Frida-objection
     https://www.52pojie.cn/forum.php?mod=viewthread&tid=1626964
     https://saucer-man.com/information_security/911.html
     https://www.cnblogs.com/my1127/p/16133663.html
     https://www.anquanke.com/post/id/197657
     https://www.cnblogs.com/ningskyer/articles/14611822.html

### 作用
    基于Frida开发的命令行工具，它可以实现不用写一行代码，便可实现诸如内存搜索、类和模块搜索、方法hook打印参数返回值调用栈等常用功能

#### 安装
     pip install objection  
     
####  命令
启动&初步命令
```text
1. objection -g 上海公交 explore        // attach 启动
    ---- 进入objection界面
2. objection -g packageName --startup-command '注入的hook逻辑'   // spawn模式
3. frida, env, help frida       // 展示的一些命令
4. 日志地址：window--C:\Users\wwj\.objection    linux--cat .objection/objection.log


其他操作
    # 打印出应用程序文件、缓存和其他目录的位置
    env
    
    # 对APP隐藏root
    android root disable 
    
    # 执行命令
    android shell_exec ls 
    
    # 截屏
    android ui screenshot /sdcard/1.png
    
    # 导入外部js脚本
    import 1.js 

Memory 指令
    memory list modules               //枚举当前进程模块
    memory list exports [lib_name]    //查看指定模块的导出函数
    memory list exports libart.so --json /root/libart.json //将结果保存到json文件中
    memory search --string --offsets-only                  //搜索内存

android heap 指令
    //堆内存中搜索指定类的实例, 可以获取该类的实例id
    search instances search instances com.xx.xx.class
     
    //直接调用指定实例下的方法
    android heap execute [ins_id] [func_name]
     
    //自定义frida脚本, 执行实例的方法
    android heap execute [ins_id]

android 指令
    android root disable   //尝试关闭app的root检测
    android root simulate  //尝试模拟root环境
    
    android ui screenshot [image.png]    //截图
    android ui FLAG_SECURE false         //设置FLAG_SECURE权限

内存漫游
    android hooking list classes    //列出内存中所有的类
     
    //在内存中所有已加载的类中搜索包含特定关键词的类
    android hooking search classes [search_name] 
     
    //在内存中所有已加载的方法中搜索包含特定关键词的方法
    android hooking search methods [search_name] 
     
    //直接生成hook某个类代码
    android hooking generate simple [class_name]

hook 方式
    /*
        hook指定方法, 如果有重载会hook所有重载,如果有疑问可以看
        --dump-args : 打印参数
        --dump-backtrace : 打印调用栈
        --dump-return : 打印返回值
    */
    android hooking watch class_method com.xxx.xxx.methodName --dump-args --dump-backtrace --dump-return
     
    //hook指定类, 会打印该类下的所有调用
    android hooking watch class com.xxx.xxx
     
    //设置返回值(只支持bool类型)
    android hooking set return_value com.xxx.xxx.methodName false

Spawn 方式 Hook
    objection -g packageName explore --startup-command '[obejection_command]'

activity 和 service 操作
    android hooking list activities           //枚举activity
    android intent launch_activity [activity_class]   //启动activity
    android hooking list services            //枚举services
    android intent launch_service [services_class]    //启动services

任务管理器
    jobs list            // 查看任务列表
    jobs kill [task_id]  // 关闭任务

关闭 app 的 ssl 校验
    android sslpinning disable

监控系统剪贴板
    // 获取Android剪贴板服务上的句柄并每5秒轮询一次用于数据。 
    // 如果发现新数据，与之前的调查不同，则该数据将被转储到屏幕上。
    help android  clipboard

执行命令行
    help android shell_exec [command]

```

### wallbreaker 插件安装&&使用
git clone https://github.com/hluwa/Wallbreaker   一般放入C:\Users\admin\.objection\\Wallbreaker

- 加载 
    
      plugin load ./Wallbreaker-master   ---- 这里window会有问题，可以切换换到 C:\Users\admin\.objection再启动objection
      
- 使用
            
  
        - plugin wallbreaker classsearch <pattern>：使用指定的模式 <pattern> 在代码中搜索类。这个命令将返回与模式匹配的所有类的列表。
        
        - plugin wallbreaker objectsearch <classname>：使用指定的类名 <classname> 在代码中搜索对象。这个命令将返回与指定类相关的所有对象的列表。
        
        - plugin wallbreaker classdump <classname> [--fullname]：将指定类 <classname> 的信息转储到文件中。如果使用了 --fullname 选项，则转储的信息将包括完整的类名。
        
        - plugin wallbreaker objectdump <handle> [--fullname]：将指定对象的信息转储到文件中。<handle> 是对象的句柄或标识符。如果使用了 --fullname 选项，则转储的信息将包括完整的类名。