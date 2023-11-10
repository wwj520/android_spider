## 基础知识点

    属性hook代码位置
    ..ratel01\app\src\main\java\com\example\ratel01\HookMysterBox3_attribute.java
    
    方法hook代码位置
      ..ratel01\app\src\main\java\com\example\ratel01\HookMysterBox4_method.java

    
### 属性值的获取
- getObjectField            获取实例属性的值
- getStaticObjectField      获取静态属性的值
- getBooleanField       
- getByteField
- getCharField
- getDoubleField
- getFloatField
- getIntField
- getLongField
- getShortField

### 属性值的修改

#### 实例属性的修改
- setObjectField          修改实例属性的值
- setBooleanField
- setByteField
- setCharField
- setDoubleField
- setFloatField
- setIntField
- setLongField
- setShortField

#### 静态属性的修改
- setStaticObjectField   
- setStaticBooleanField
- setStaticByteField
- setStaticCharField
- setStaticDoubleField
- setStaticFloatField
- setStaticIntField
- setStaticLongField
- setStaticShortField

## 实例
#### hook 属性  
    ratel01\app\src\main\java\com\example\ratel01\HookMysterBox3_attribute.java
```jupyter
RposedHookLoadPackage {
    private static final String TAG = "yuanrenxue-->";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.example.mysterbox")){
            RposedHelpers.findAndHookConstructor("com.example.mysterbox.MysterBox1", lpparam.classLoader, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    Object box = param.thisObject;
                    Log.d(TAG, "afterHookedMethod:" + box); // afterHookedMethod:MysterBox1{content='普通', isOpened=false, price=10, brand='bbs', text='null'}


                    // 1. 获取实例属性的值： getObjectField(对象, 对象属性名)
                    //  public static <T> T getObjectField(Object obj, String fieldName)
                    Object content = RposedHelpers.getObjectField(box, "content");
                    Log.d(TAG, "getObjectField: "+ content);

                    // 2.获取静态属性：getStaticObjectField
                    // public static Object getStaticObjectField(Class<?> clazz, String fieldName)
                    Object base_price = RposedHelpers.getStaticObjectField(box.getClass(), "base_price");
                    Log.d(TAG, "getStaticObjectField: "+ base_price);

                    // 3.修改实例属性的值：
                    // public static void setObjectField(Object obj, String fieldName, Object value)
                    RposedHelpers.setObjectField(box, "content", "大禹文化");
                    RposedHelpers.setIntField(box, "price", 10000);

                    //4.修改静态属性的值：在这打印的静态属性显示时候不会显示为修改后的，通过jadx反编译可以看到
                    //public static void setStaticBooleanField(Class<?> clazz, String fieldName, boolean value)
                    RposedHelpers.setStaticObjectField(box.getClass(), "base_price", 500);


                }
            });


        }
    }
}
```

#### hook 方法
    D:\AndroidStudioProjects\ratel01\app\src\main\java\com\example\ratel01\HookMysterBox4_method.java
    
    静态函数hook
    实例函数hook
    
    内部类的处理
    Java层JNI函数hook

```jupyter
public class HookMysterBox4_method implements IRposedHookLoadPackage {
    private static final String TAG = "yuanrenxue----------->";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.example.mysterbox")){
            Log.d(TAG, "handleLoadPackage: hook method success");

            // hook 静态方法---两种
            // findAndHookMethod(String className, ClassLoader classLoader, String methodName, Object... parameterTypesAndCallback)
            RposedHelpers.findAndHookMethod("com.example.mysterbox.MysterBox1", lpparam.classLoader, "staticMethod", String.class, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                    Log.d(TAG, "beforeHookedMethod: 参数1:"+param.args[0]+ "参数2:"+param.args[1]);
                    // 修改参数值
                    param.args[0] = "kopbi";
                    param.args[1] = 6000;

                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    //获取方法返回值
                    Log.d(TAG, "afterHookedMethod:"+param.getResult());

                    // 修改方法返回值，返回值类型要和原始的保持一致
                    param.setResult("修改了静态方法返回值");

                }
            });

            // hook 实例方法
            //findAndHookMethod(Class<?> clazz, String methodName, Object... parameterTypesAndCallback)
            Class<?> MysterBox = lpparam.classLoader.loadClass("com.example.mysterbox.MysterBox1");
            RposedHelpers.findAndHookMethod(MysterBox, "instanceMethod", String.class, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                    Log.d(TAG, "beforeHookedMethod-实例: 参数1:"+param.args[0]+ "参数2:"+param.args[1]);
                    param.args[0] = "实例方法";
                    param.args[1] = 3000;

                }


                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);

                }
            });

            // hook内部类的处理：
            // 类名这样获取--类名$内部类类名-----"com.example.mysterbox.MysterBox1$InnerClass"
            RposedHelpers.findAndHookMethod("com.example.mysterbox.MysterBox1$InnerClass", lpparam.classLoader, "innerClassMethod", String.class, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                    Log.d(TAG, "内部类: 参数1:"+param.args[0]+ "参数2:"+param.args[1]);
                    // 修改参数值
                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    Log.d(TAG, "afterHookedMethod-内部类结果:"+param.getResult());

                }
            });

        };


    }
}

```    
## 补充：
#### 如何在已有项目中添加jni的⽀持

- 步骤

      1. 在main⽂件夹下⾯创建 cpp ⽂件夹
      2. 在cpp⽂件夹下⾯添加 CMakeLists.txt
      ```
        # For more information about using CMake with Android Studio, read the
        # documentation: https://d.android.com/studio/projects/add-native-code.html
        # Sets the minimum version of CMake required to build the native library.
        cmake_minimum_required(VERSION 3.10.2)
        # Declares and names the project.
        project("native-lib")
        # Creates and names a library, sets it as either STATIC
        # or SHARED, and provides the relative paths to its source code.
        # You can define multiple libraries, and CMake builds them for you.
        # Gradle automatically packages shared libraries with your APK.
        add_library( # Sets the name of the library.
                native-lib
                # Sets the library as a shared library.
                SHARED
                # Provides a relative path to your source file(s).
                native-lib.cpp
                )
        # Searches for a specified prebuilt library and stores the path  as a
        # variable. Because CMake includes system libraries in the search path by
        # default, you only need to specify the name of the public NDK library
        # you want to add. CMake verifies that the library exists before
        # completing its build.
        find_library( # Sets the name of the path variable.
                log-lib
                # Specifies the name of the NDK library that
                # you want CMake to locate.
                log)
        # Specifies libraries CMake should link to your target library. You
        # can link multiple libraries, such as libraries you define in this
        # build script, prebuilt third-party libraries, or system libraries.
        target_link_libraries( # Specifies the target library.
                native-lib
                # Links the target library to the log library
                # included in the NDK.
                ${log-lib})
      ```
      3. 在 app 的 build.gradle ⽂件下⾯添加
            android {
                externalNativeBuild {
                    cmake {
                    path "src/main/cpp/CMakeLists.txt"
                    version "3.10.2"
                    }
                }
            }
       4 重新加载build.gradle配置， 这时候如果在接下来写cpp文件时候发现有报错，基本是缺少对应的Cmake文件，下载一个

  
#### JNI编程模型的结构
HOOK-native的方法和普通方法基本相同

    Java层声明Native方法。
    JNI层实现Java层声明的Native方法，在JNI层可以调用底层库或者回调Java层方法。这部分将被编译为动态库(SO文件)供系统加载。
    加载JNI层代码编译后生成的共享库。

- 代码&&步骤

  1. 先在java层声明Native方法
   ```jupyter
      private native String nativeMethod();
    ```
   2.JNI层实现Java层声明的Native方法，【首先在 cpp 文件夹下创建native-app.cpp文件】
   - demo
   ```jupyter
          #include <jni.h>
          #include <string>
        
         extern "C"
         JNIEXPORT jstring JNICALL
         Java_com_example_mysterbox_MainActivity_nativeMethod(JNIEnv *env, jobject thiz) {
            // TODO: implement nativeMethod()
            std::string message = "我是一个nativeMethod函数";
            return env->NewStringUTF(message.c_str());
        };
    ```

