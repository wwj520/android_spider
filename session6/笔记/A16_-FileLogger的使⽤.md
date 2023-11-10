## 目录

#### FileLogger的⽤途
- 防⽌⽇志过多logcat存不开
- 保存⽇志，在有需要的时候可以查看
- 使用步骤
```text
1. 在hook脚本中插入：
    FileLogger.startRecord(RatelToolKit.sContext.getFilesDir());
    
    eg: code位置：..\ratel01\app\src\main\java\com\example\ratel01\FileLoggerEntry.java
        
        public class FileLoggerEntry implements IRposedHookLoadPackage {
            private static final String TAG = "yuanrenxue";
        
            @Override
            public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
                Log.d(TAG, "handleLoadPackage: success");
                FileLogger.startRecord(RatelToolKit.sContext.getFilesDir());
                FileLogger.outLog("这是测试日志");        // 输出写好的日志
                FileLogger.outTrack(TAG);               // 输出堆栈信息
                /*
                    这里如果手机没root权限的，可以通过RPC-AppiumEntry脚本中，调用FileExploreHandler，直接从路由中获取日志
                    eg: 127.0.0.1/5612?group=ratel-appium&action=fileExplore
                */
                 FileLogger.stopRecord();
            }
        }
        
2. FileLogger.stopRecord();
```
- 输出⽇志到⽂件
```text
public static void outLog(final String message);
public static void outLog(final InputStream inputStream);
public static void outLog(final byte[] data);
public static void outLog(final String tag, final String message);
public static void outLog(final String tag, final InputStream inputStream);
public static void outLog(final String tag, final byte[] data);
public static void outTrack(String append);
```
  
  
#### sshdroid的使⽤
- 作用
```text
    给android app提供的一个sshd服务，起主要作用是提供一个交互式的shell工具， 我们可以通过他访问app的内部数据文件。
    在Android上开启ssh服务，可以export ⽂件系统操作app私有⽂件，⽽不需要root权限。
```

- 使用流程
```text
1. 下载源码安装： https://github.com/virjarRatel/sshdroid
2. 复制文件: app/src/main/assets/config.template.properties->  app/src/main/assets/config.properties
3. 修改内容
		targetPackage: 需要被注入的进程
		ssdServerPort: 启动的端口号，请注意不要和其他服务冲突
		newProcess: 是否需要在新进程中启动,如果你的app开启了分身，那么最好将这个配置设置为true。因为分身功能将会破坏原有文件系统(特别是平头哥系统)
4. 安装并运行插件
5. 在电脑上面运行adb forward,如： adb forward tcp:3478 tcp:3478
6. 使用电脑连接服务，如：
	ssh 127.0.0.1 -p 3478 登陆shell
	scp -P 3478 ./test.txt 127.0.0.1:/data/data/xxx/files/ -----------------下载服务1
	scp -P 3478 127.0.0.1:/data/data/xxx/files/aaa.log ~/Desktop/  -----------------下载服务2




```