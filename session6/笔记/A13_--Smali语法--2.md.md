## 目录 

#### 数据的定义

- 概括
```jupyter
    
    java类型     取值关键字           赋值关键字
    -------------------------------------------
    byte          iget-byte             iput-byte
    short         iget-short            iput-short
    int             iget                  iput
    float           iget                  iput
    long           iget-wide            iput-wide
    double         iget-wide            iput-wide
    char           iget-char             iput-char
    boolean        iget-boolean         iput-boolean
```

- 常量
```jupyter
const v0, 30 将30赋值给v0寄存器 占⽤⼀个寄存器
const-wide v0,30 这⾥占⽤两个寄存器v0和v1


Demo:
    JAVA :
        public class Demo extends Activity {
            Demo(){
                int a = Integer.MAX_VALUE;
                int b = 100;
                boolean x = true;
                long y = Long.MAX_VALUE;
            }
    Smail:
        # direct methods
        .method constructor <init>()V
            .registers 7
        
            .prologue
            .line 10
            invoke-direct {p0}, Landroid/app/Activity;-><init>()V
        
            .line 11
            const v0, 0x7fffffff
        
            .line 12
            .local v0, "a":I
            const/16 v1, 0x64
        
            .line 13
            .local v1, "b":I
            const/4 v2, 0x1
        
            .line 14
            .local v2, "x":Z
            const-wide v4, 0x7fffffffffffffffL
        
            .line 17
            .local v4, "y":J
            return-void
        .end method
         
            

}

```

- 静态字段赋值
```jupyter
语法规则：sput-object v0, 被赋值全类名路径;->变量名;变量全类名路径

java:
    private static String a;
    Demo() {
        a = "yuanrenxue";
    }

smail:
     const-string v0, "yuanrenxue"
     sput-object v0, Lcom/example/ratel02/smali/Demo;->a:Ljava/lang/String;
```

- ⾮静态字段赋值
```jupyter
- java
    private  String a;
    Demo() {
        a = "yuanrenxue";
    }

- smail
     const-string v0, "yuanrenxue"

    iput-object v0, p0, Lcom/example/ratel02/smali/Demo;->a:Ljava/lang/String;
```
- 静态字段取值



- ⾮静态字段取值  


####  逻辑语句
````jupyter
if-eq vA, vB, :cond_xx 如果vA等于vB跳转到cond_xx
if-ne vA, vB, :cond_xx 如果vA 不等于vB跳转到cond_xx
if-lt vA, vB, :cond_xx 如果vA⼩于vB跳转到cond_xx
if-le vA, vB, :cond_xx 如果vA⼩于等于vB跳转到cond_xx
if-ge vA, vB, :cond_xx 如果vA⼤于等于vB跳转到cond_xx
if-gt vA, vB, :cond_xx 如果vAd⼤于B跳转到cond_xx
if-eqz vA, :cond_xx 如果vA等于0跳转到cond_xx
if-nez vA, :cond_xx 如果vA不等于0跳转到cond_xx
if-ltz vA, :cond_xx 如果vA⼩于0跳转到cond_xx
if-lez vA, :cond_xx 如果vA⼩于等于0跳转到cond_xx
if-gez vA, :cond_xx 如果vA⼤于等于0跳转到cond_xx
if-gtz vA, :cond_xx 如果vA⼤于0跳转到cond_xx
````


#### 循环语句
```jupyter
JAVA : 
        public class Demo{
        Demo(){
            for (int i=0; i < 10; i++){
    
            }
        };
    }


SMAIL:

        .method constructor <init>()V
            .registers 3
        
            .prologue
            .line 11
            invoke-direct {p0}, Ljava/lang/Object;-><init>()V
        
            .line 12
            const/4 v0, 0x0
        
             # 定义i=0
            .local v0, "i":I
            :goto_4
            # 定义了常量 10
            const/16 v1, 0xa
            # 判断条件：if v0>=v1,跳转到cond_b语句
            if-ge v0, v1, :cond_b
            # 如果上面的判断失败. 则v0自增1
            add-int/lit8 v0, v0, 0x1
        
            goto :goto_4
        
            .line 15
            :cond_b
            return-void
        .end method

```


#### RDP的使⽤
- 作用
```text
    可以对apk进⾏源码级别修改的模块。在apktool对现代app重打包⽆效之后，⼏乎没有出现可以对apk进⾏smali修改的框架出现
```

- ratel.bat存储位置：
    D:\all_python_study\yuanrenxue_android_code\session6\tools\ratel-engine
    
- 使用流程
    1. rdp⼯程产⽣      ----- ./ratel.bat -D xxx.apk 
    2. rdp修改smali
    3. rdp回编为apk    -----   ratel_resource/rdp.bat 启动
