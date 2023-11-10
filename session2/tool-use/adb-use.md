- 文章：https://blog.csdn.net/weixin_43847093/article/details/84673414

- 基本使用：
    ```html
    adb devices --- 
    adb shell getprop ro.product.cpu.abi         // 查看手机架构
    
    adb shell "dumpsys window | grep mCurrentFocus" // 查看当前运行的activity  可能需要先adb进入su
  
  
    ```

