## Demo：
       MysterBox项目下 MysterBox1+ MysterBox\app\src\test\ExampleUnitTests测试类
       

## JAVA反射
#### 获取类的对象
-  类名.class
-  通过对象获取 对象.getClass()
-  通过全类名获取 Class.fromName(全类名)
-  classLoader.loadClass(全类名)
```jupyter
    @Test
    public void getClassDemo() throws Exception {
        //1. 通过类直接获取类对象
        Class<?> class1 = MysterBox1.class;
        System.out.println(class1);

        //2 通过对象获取   对象.getClass()
        MysterBox1 box = new MysterBox1();
        Class<?> aClass = box.getClass();
        System.out.println(aClass);

        //3.1 通过全类名获取---Class.forName(全类名)
        Class<?> aClass1 = Class.forName("com.example.mysterbox.MysterBox1");
        System.out.println(aClass1);
        
        //3.2 通过全类名获取---ClassLoader.loadClass(全类名)
        ClassLoader systemClassLoader = ClassLoader.getSystemClassLoader();
        Class<?> aClass2 = systemClassLoader.loadClass("com.example.mysterbox.MysterBox1");
        System.out.println(aClass2);
    }

```


#### 判断是否为某个类的实例
- 实例 instanceof 类名 
- 类 名.class.isInstance(类对象)
- 对象.getClass().isAssignableFrom(类名.class)
```jupyter
    @Test
    public void isInstanceDemo() {

        // 1.instanceof 关键字
        MysterBox1 box = new MysterBox1();
        System.out.println(box instanceof MysterBox1);


        // 2. 类名.class.isInstance(实列对象)
        System.out.println(MysterBox1.class.isInstance(box));

        // 3.对象.getClass().isAssignableFrom(类名.class)
        System.out.println(box.getClass().isAssignableFrom(MysterBox1.class));
    }


```
#### class相关
- getClassLoader 获取类加载器
- getClasses     返回该类当中所有的公共类和接口的对象数组
- getDeclaredClasses 返回该类当中的所有类和结构的对象数组
- getName 获取类的全类名
- newInstance  创建实例走默认的无参构造函数
```jupyter
    @Test
    public void createInstance() throws Exception {
        Class<?> mysteryBoxClass = MysterBox1.class;

        // 1.newInstance：会优先调用自己构造函数，如果没有则调用默认的无参构造函数
        /*
            使用 mysteryBoxClass 的实例化方法 newInstance() 创建一个 MysterBox1 类的实例，并将其赋值给 box1 变量。
            由于 newInstance() 方法返回的是一个 Object 类型的对象，所以需要进行类型转换为 MysterBox1 类型。
        */
        MysterBox1 box1 = (MysterBox1) mysteryBoxClass.newInstance();
        System.out.println(box1.getContent( ));


        // 2. 首先把获取到构造器，然后实例化类对象
        Constructor<?> constructor = mysteryBoxClass.getConstructor();
        Object box2 = constructor.newInstance();
        System.out.println(box2);  // com.example.mysterbox.MysterBox1@1750fbeb
    }
```

#### Field 类
- getField(“属性名")只能获取到public的
- getName  获取属性名
- getModifiers  获取修饰符
- set(对象,属性值)设置属性值
- getDeclaredField(“属性名") 获取private属性
- setAccessible(true) 设置属性的可访问属性
```jupyter

    @Test
    public void  getMemberVariables() throws  Exception{
        MysterBox1 box1 = new MysterBox1();

        // 1.getField--获取public修饰的指定成员变量
        Field priceField = MysterBox1.class.getField("price");
        System.out.println(priceField.get(box1));

        // 2. getFields获取public修饰的所有成员变量
        Field[] priceFields = MysterBox1.class.getFields();
        for (Field field : priceFields) {
            System.out.println(field.getName() + ": " + field.get(box1));

        }

        // 3. getDeclaredField 获取private修饰的指定成员变量, 需要设置setAccessible
        Field contnent1 = MysterBox1.class.getDeclaredField("content");
        contnent1.setAccessible(true);
        System.out.println(contnent1.get(box1));

        // 4.getDeclaredFields
        Field[] Fields = MysterBox1.class.getDeclaredFields();
        for (Field field : Fields) {
            field.setAccessible(true);
            System.out.println(field.getName() + "**: " + field.get(box1));
        }
    }


```

#### Method类
- getMethod(方法名,参数类型(eg:Sting.class)  ) 获取public方法
- getMethods 获取所有方法
- getDeclaredMethod(方法名，参数类型) 获取方法
- getDeclaredMethods 获取所有方法
- invoke(对象,参数列表) 执行方法
```jupyter

    @Test
    public void getMethod() throws Exception {
        MysterBox1 box1 = new MysterBox1();


        // 1.getMethod后需要使用 invoke(实列)
        Method getMethod1 = MysterBox1.class.getMethod("getContent");
        System.out.println(getMethod1.invoke(box1));

        // 2 getMethods
        Method[] methods = MysterBox1.class.getMethods();
        for (Method method : methods) {
//            System.out.println(method);

        }

        // 3.getDeclaredMethod -- 可以获取private定义的方法
        box1.open();
        System.out.println(box1.getContent());
        Method close = MysterBox1.class.getDeclaredMethod("close"，参数类型1， 参数类型2);
        close.setAccessible(true);
        close.invoke(box1, 参数1， 参数2);
        System.out.println(box1.getContent());


        // 4. getDeclaredMethods -- 可以获取所有的方法
        Method[] closes = MysterBox1.class.getDeclaredMethods();
        for (Method method : closes) {
            System.out.println(method.getName());
        }


    }



```

#### 构造方法Constructor
- Class对象.getConstructors 获取构造方法列表
- Class对象.getConstructor(parameterTypes) 获取构造方法 
- getConstructor,getConstructors 只能获取public的构造函数
- getDeclaredConstructord 获取 private 的构造函数
 - getDeclaredConstructords 获取 所有的构造函数
````jupyter
    @Test
    public void getConstructors() throws Exception {
        /*
            *******************************
            1. getConstructor,getConstructors 只能获取public的构造函数
            2. getDeclaredConstructord 获取 private 的构造函数
            3. getDeclaredConstructords 获取 所有的构造函数
            ******************************
        */

        // 1. getConstructor
        Constructor<?> constructor = MysterBox1.class.getConstructor(int.class);
        System.out.println(constructor);  // public com.example.mysterbox.MysterBox1(int)
        System.out.println(constructor);  // public com.example.mysterbox.MysterBox1(int)


        // 2.getConstructors 获取所有的构造函数
        Constructor<?>[] constructors = MysterBox1.class.getConstructors();
        System.out.println(Arrays.toString(constructors));

        // 3.getDeclaredConstructord 获取private的构造函数
        Constructor<?> declaredConstructor = MysterBox1.class.getDeclaredConstructor(String.class);
        System.out.println(declaredConstructor);
        Constructor<?>[] declaredConstructors = MysterBox1.class.getDeclaredConstructors();
        System.out.println(Arrays.toString(declaredConstructors));

    }
````


## 实例(盲盒项目) 使用平头哥插件Hook构造函数
    ..MysterBox\app\src\main\java\com\example\mysterbox\MysterBox1.java
- 知识点-在平台哥插件种的代码
```text

// 判断包名是否等下xxxx.xxx
pparam.packageName.equals("com.example.mysterbox")

// Hook构造函数
RposedHelpers. findAndHookConstructor(Class<?> clazz, Object... parameterTypesAndCallback)
RposedHelpers. findAndHookConstructor(String className, ClassLoader classLoader, Object... parameterTypesAndCallback)

```
- 步骤
```text






```



```jupyter
package com.example.ratel01;

import android.util.Log;

import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

public class HookMysterBox implements IRposedHookLoadPackage {
    private static final String TAG = "mysterboxHook-->";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.example.mysterbox")){
            Log.d(TAG, "hook success");

            /*
                hook一个构造函数: 两种
                findAndHookConstructor(Class<?> clazz, Object... parameterTypesAndCallback)
                findAndHookConstructor(String className, ClassLoader classLoader, Object... parameterTypesAndCallback)
            */

            // 1. 先获取到类示例
            Class<?> MysteryBox = lpparam.classLoader.loadClass("com.example.mysterbox.MysterBox1");
            RposedHelpers.findAndHookConstructor(MysteryBox, new RC_MethodHook() {

                // 构造方法之前回调
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    Object[] objects = param.args;
                    Log.d(TAG, "len="+objects.length);
                    super.beforeHookedMethod(param);
                }

                // 构造方法之后回调
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                }
            });


            // 2.直接通过全类名:
            // int.class 是使用了构造函数有一个int参数的
            RposedHelpers.findAndHookConstructor("com.example.mysterbox.MysterBox1", lpparam.classLoader, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    Log.d(TAG, "price="+param.args[0]);
                    param.args[0] = 2000;
                    super.beforeHookedMethod(param);
                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    // 获取构造函数返回是实例
                    Log.d(TAG, "afterHookedMethod:" + param.thisObject + "," + param.getResult());//com.example.mysterbox.MysterBox1@7e6cd47,null

                }
            });


        }
    }
}







```






