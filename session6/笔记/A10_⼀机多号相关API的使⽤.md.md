### 1 刷机
````text
1. android 下载地址：https://developers.google.cn/android/images?hl=zh-cn#angler
2. 执行命令 : ⼿机启动到BootLoader模式 --- adb reboot bootloade

````
### 2.Android相关硬件指纹获取
- 指纹参考：https://github.com/song-dev/device-info
- 安装依赖
```text
1. 清单文件【AndroidManifest.xml】中添加：
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    
2.  app-build.gradle:
        dependencies {
            implementation 'com.github.getActivity:XXPermissions:13.5'
        }
3.  project-build.gradle:
        buildscript {
            repositories {
                ...
                maven { url 'https://jitpack.io'}
            }
        }

        allprojects {
            repositories {
               .....
               maven { url 'https://jitpack.io'}
            }
        }

```
-  部分指纹代码【待补充】
```jupyter

---- IMEI
    @SuppressLint("HardwareIds")
    private String getIMEI() {
        try {
            TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
            return tm.getDeviceId();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return "-";
    }
    
    
----- 设备序列号(SERIAL)
 @SuppressLint("HardwareIds")
    private String getAndroidId() {
        try {
            return Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDRO
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return "-";
    }
```
### 3. Ratel virtualEnv(虚拟环境) 相关API

- 模块介绍：import com.virjar.ratel.api.RatelToolKit;
- VirtualEnvModel：表ratel框架⽀持的集中虚拟化设备模式
```jupyter
    VirtualEnvModel对应的值如下：
        1. DISABLE：未启⽤虚拟环境
        2. START_UP：每次启动app切换设备数据
        3. INSTALL：app重新安装的时候切换设备数据，适合登录态+不会编程控制
        4. Multi：多⽤户模式，这个模式⽐较特殊，将会放⼤⽤户。通过时间分割的⽅式实现多⽤户
                【开启Multi修改用户时候，确保app是打开状态】

```
- 接口：
 
        com.virjar.ratel.api.VirtualEnv#switchEnv          
        com.virjar.ratel.api.VirtualEnv#nowUser
        com.virjar.ratel.api.VirtualEnv#availableUserSet
        com.virjar.ratel.api.VirtualEnv#removeUser


- 使用步骤
````jupyter

1.  在清单文件中添加
        
   <meta-data
        android:name="virtualEnvModel" // 注意大小写
        android:value="Multi"
    />
2. Demo1: 
     code地址：{
        ...\ratel01\app\src\main\java\com\example\ratel01\VirtualEnvEntry.java
     }
     示例：{
          Log.d(TAG, "handleLoadPackage: user" + RatelToolKit.virtualEnv.nowUser());           // 获取当前用户 
        
          Log.d(TAG, "handleLoadPackage: user" + RatelToolKit.virtualEnv.availableUserSet());  // 获取所有用户
     }

     
2. Demo2     
    code地址：{
            ...\ratel01\app\src\main\java\com\example\ratel01\VirtualEnvEntry.java
            ... \ratel01\app\src\main\java\com\example\ratel01\handlers\VirtualswitchEnvHandler.java
         }
      RatelToolKit.virtualEnv.switchEnv(userId); // 传入 userId需要满⾜JavaIdentify规则（数字、字⺟、下划线）  
   ·1



````









     
