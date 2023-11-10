## 目录 

#### 杂记
````jupyter
git： https://github.com/ollide/intellij-java2smali
as插件：  java2smail
````

####  Smali和Java的基本数据类型
```jupyter
smali       java
B             byte
S             short
I             int
J             long
F             float
D             double
C             char
Z             boolean
V             void
[            数组

L + ⽤ / 分割的全类名路径  object
```
#### Smail 相关声明 
- 类声明 
```jupyter
语法规则: .class + 权限修饰符 + 全类名;
demo:
    java:
        package com.example.ratel02.smali;
            import java.io.Serializable;
            public class Demo implements Serializable {}
    
    smail： 
         .class public Lcom/example/ratel02/smali/Demo;
        .super Ljava/lang/Object;
        .source "Demo.java"
        
        # interfaces  这里java类里面实现了接口，所有会有这一项
        .implements Ljava/io/Serializable;        

```
- 字段声明
```jupyter
语法规则: .field 权限修饰符 + 静态修饰符(如果是静态的) + 变量名: 全类名路径;

demo:
    java:
        package com.example.ratel02.smali;
        import java.io.Serializable;
        public class Demo implements Serializable {
            private static String aString;
            private int aInt;
            public long aLong;
    
    smail： 
        .# static fields 注意静态的最后面有---->;
        .field private static aString:Ljava/lang/String;
        
        # instance fields
        .field private aInt:I
     
        .field public aLong:J
       
```
- 常量声明
```jupyter
语法规则: .field 权限修饰符 + [静态修饰符] + final + 变量名: 全类名路径; = 常量值

demo:
    java:
        public class Demo implements Serializable {
            private  static  final String aString = "yuanrenxue";
            }
    
    smail： 
        # static fields
        .field private static final aString:Ljava/lang/String; = "yuanrenxue"
       
```
- ⽅法/函数的声明 + 返回值与数据类型对应关系
    
        返回关键字                                 Java数据类型  
        return                                 byte  hort int float char boolean
        return-wide                            long double
        return-void                            void
        return-object                          数组 object
 
```jupyter
语法规则: 
    .method 权限修饰符 + [静态修饰符] + ⽅法名(参数类型)返回值类型
    # ⽅法体
    .end method # ⽅法结束标记
    
demo:
    java:
            private static void f1(){}
            private static String f2(String X) {
                return "wwj";
            }
            public int f3(){
                return 1;
            }
            private long f4() {
                return 0L;
            }
            
     smail：        
            .method private static f1()V
                .registers 0
            
                .prologue
                .line 7
                return-void
            .end method
            
            .method private static f2(Ljava/lang/String;)Ljava/lang/String;
                .registers 2
                .param p0, "X"    # Ljava/lang/String;
            
                .prologue
                .line 10
                const-string v0, "wwj"
            
                return-object v0
            .end method
            
            .method private f4()J
                .registers 3
            
                .prologue
                .line 18
                const-wide/16 v0, 0x0
            
                return-wide v0
            .end method
            
            
            # virtual methods
            .method public f3()I
                .registers 2
            
                .prologue
                .line 14
                const/4 v0, 0x1
            
                return v0
            .end method
                    
    
    


```


- 构造函数的声明、静态代码块的声明
```jupyter
构造函数:
   .method 权限修饰符 + constructor <init>(参数类型)V
    # ⽅法体
    .end method


静态代码块:
    .method static + constructor <clinit>()V
    # ⽅法体
    .end method
```

#### ⽅法调⽤
 
- 关键字
```jupyter
invoke-virtual      ⾮私有实例⽅法的调⽤
invoke-direct       构造⽅法&&及私有⽅法的调⽤
invoke-static       静态⽅法的调⽤
invoke-super        ⽗类⽅法的调⽤
invoke-interface    接⼝⽅法的调⽤

```    
- ⾮私有实例⽅法的调⽤

```jupyter
语法规则: invoke-virtual {参数}, ⽅法所属类名;->⽅法名(参数类型)返回值类型;

demo:
    java:
        package com.example.ratel02.smali;
            import java.io.Serializable;
            public class Demo implements Serializable {}
    
    smail： 
        # direct methods
        .method constructor <init>(Ljava/lang/String;)V
            .registers 2
            .param p1, "A"    # Ljava/lang/String;
        
            .prologue
            .line 8
            invoke-direct {p0}, Ljava/lang/Object;-><init>()V
        
            .line 9
            invoke-virtual {p0}, Lcom/example/ratel02/smali/Demo;->func()Ljava/lang/String;
        
            .line 10
            return-void
        .end method


```

- 静态方法、私有方法、构造函数的调用与【⾮私有实例⽅法的调⽤】类似

- ⽗类⽅法的调⽤

```jupyter

语法规则: invoke-super {参数}, ⽅法所属类名;->⽅法名(参数类型)返回值类型;

java:
    public class Demo extends Activity {
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        }
    }
    
smail：
    # virtual methods
    .method protected onCreate(Landroid/os/Bundle;)V
        .registers 2
        .param p1, "savedInstanceState"    # Landroid/os/Bundle;
            .annotation build Landroidx/annotation/Nullable;
            .end annotation
        .end param
    
        .prologue
        .line 12
        invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    
        .line 13
        return-void
    .end method
 
```
- 接⼝的调⽤
```jupyter

语法规则: invoke-interface {参数}, ⽅法所属类名;->⽅法名(参数类型)返回值类型;

- java: 
    public class Demo extends Activity {
    // 定义实现类
    public static class Demo2 implements Callback {
        @Override
        public void test() {
        }
    }
    // 测试类调用
    Demo() {
        Callback demo2 = new Demo2();
        demo2.test();
    }
    // 声明接口
    interface Callback {
        void test();
    }

}

- smail:

    # direct methods
    .method constructor <init>()V
        .registers 2
    
        .prologue
        .line 17
        invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    
        .line 18
        new-instance v0, Lcom/example/ratel02/smali/Demo$Demo2;
    
        invoke-direct {v0}, Lcom/example/ratel02/smali/Demo$Demo2;-><init>()V
    
        .line 19
        .local v0, "demo2":Lcom/example/ratel02/smali/Demo$Callback;
        invoke-interface {v0}, Lcom/example/ratel02/smali/Demo$Callback;->test()V
    
        .line 20
        return-void
    .end method
     






```


