### apktool反编译工具使用

#### 使用
        下载apktool.jar:  https://apktool.org/
        编写apktool.bat 
        一般将这两文件直接放在 C:\Windows 目录下 
##### 命令
 
     apktool d com.test.apk      反编译apk包

     apktool b com.test         重打包成aa
     
#### 生成签名
    1.. 确保你已经安装了 Java Development Kit (JDK) 和 Android SDK，并且已经配置好了相应的环境变量。
    2. 使用 apktool 命令重新打包 APK 文件。假设你的 APK 文件名为 app.apk，可以使用以下命令：
            apktool b app -o new_app.apk
    3. 生成一个新的签名证书。可以使用以下命令生成一个新的 keystore 文件：
            keytool -genkey -v -keystore my-release-key.keystore -alias my-alias -keyalg RSA -keysize 2048 -validity 10000
    4. 使用 jarsigner 命令对新生成的 APK 文件进行签名。假设你的 keystore 文件名为 my-release-key.keystore，可以使用以下命令：
            arsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore new_app.apk my-alias
    5. 最后，使用 adb install 命令安装重新签名的 APK 文件。假设你的新 APK 文件名为 new_app.apk，可以使用以下命令：
            db install new_app.apk
    

### 杂技
- 1. AndroidKiller.exe 中可以直接使用apktool是修改源码（smail语言）
    
     
     
