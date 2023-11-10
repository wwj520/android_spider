### 平头哥框架⾃动化 SupperAppium

####  相关概念
- PageTriggerManager
```text
PageTriggerManager管理了android⻚⾯切换事件、管理⾃动化驱动扩展逻辑。

PageTriggerManager监控了Activity、Fragment、Dialog、PopupWindow的⽣命周期

PageTriggerManager不⽀持webview，但是可以通过com.virjar.ratel.api.extension.superappium.WebViewHelper进⾏浏览器的⾃动化操作监控
```
- ViewImage

```text
    他是SupperAppium的界⾯元素的节点封装，dom tree的node。在android原⽣的view对象上⾯封装了
DOM函数(parent、child、siblings、index、attributes等)，封装了xpath操作函数，封装了滑动相关函
数、封装了点击和type(⽂字输⼊)等函数。他是我们⾃动化编程的核⼼API。

```
#### 实例&步骤

1. 新写一个新的布局& Activity

        .. \CourseSix\app\src\main\res\layout\activity_login.xml

2. 主 Activity

         ..\CourseSix\app\src\main\java\com\yuanrenxue\course6\C11LoginActivity.java
    ```text
    public class C11LoginActivity extends AppCompatActivity implements View.OnClickListener {
        private EditText name;
        private EditText password;
    
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_login);
    
            name = findViewById(R.id.name);
            password = findViewById(R.id.password);
            findViewById(R.id.login).setOnClickListener(this);
    
        }
    
        @Override
        public void onClick(View v) {
            String username = name.getText().toString();
            String password1 = password.getText().toString();
            if ("jackwu".equals(username) && "123456".equals(password1)) {
                // 点击后提示
                Toast.makeText(this, "登录成功", Toast.LENGTH_LONG).show();
            }else{
                Toast.makeText(this, "登录失败", Toast.LENGTH_LONG).show();
            }
        }
    ```

3. 写 一个hook类
```text
code地址：..\ratel01\app\src\main\java\com\example\ratel01\LoginActionHandlerEntry.java
---------------------------------------------------------------------------------------------------
public class LoginActionHandlerEntry implements IRposedHookLoadPackage {
    private static final String TAG = "YUANRENXUE";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        Log.d(TAG, "handleLoadPackage: ");
        // 延迟
        PageTriggerManager.trigger(3000);
        // 入口类----LoginActionHandler 需要引用的handler
        PageTriggerManager.addHandler("com.yuanrenxue.course6.LoginActivity", new LoginActionHandler());
    }
}

```
 
4. 写SupperAppium-handler
```text
code地址：..\ratel01\app\src\main\java\com\example\ratel01\handlers\LoginActionHandler.java
---------------------------------------------------------------------------------------------------
package com.example.ratel01.handlers;
import android.app.Activity;
import android.util.Log;
import android.webkit.WebView;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;
import com.virjar.ratel.api.extension.superappium.WebViewHelper;


public class LoginActionHandler implements PageTriggerManager.ActivityFocusHandler {
    private static final String TAG = "yuanrenxue";

    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        Log.d(TAG, "handleActivity: ");
        // demo1: 自动登录
        root.typeByXpath("//android.widget.EditText[@id='com.yuanrenxue.course6:id/name']", "jackwu");
        root.typeByXpath("//android.widget.EditText[@id='com.yuanrenxue.course6:id/password']", "123456");
        root.clickByXpath("//android.widget.Button[@id='com.yuanrenxue.course6:id/login']");

        // demo2： webview搜索功能
        WebView webView = root.findWebViewIfExist();
        if (webView == null) {
            Log.d(TAG, "handleActivity: not find web view");
            return false;
        }
        WebViewHelper.JsCallFuture jsCallFuture = new WebViewHelper(webView).typeByXpath("例如：搜索框xpth", "搜索与的内容");
        jsCallFuture.success().clickByXpath("点击的xpath按钮");
        // demo2：处理异常
        jsCallFuture.failed(new WebViewHelper.OnJsCallFinishEvent() {
            @Override
            public void onJsCallFinished(String callResultId) {
                // 延迟操作
                PageTriggerManager.trigger(400);

            }
        });
        // return true时只执行一次
        return true;
    }
}





```        
         
         
         
