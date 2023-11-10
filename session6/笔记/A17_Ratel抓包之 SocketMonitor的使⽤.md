## 目录
#### SocketMonitor 的作⽤
```text

    流量拦截是ratel⽀持的⼀种基于socket对象监控的抓包⽅案。他可以直接拦截所有tcp流量，包括SSL。
同时不需要考虑SSL证书，http代理⽆法⽣效等问题，并且在在抓包的同时，可以通过堆栈回溯⽅法知
道⽹络流量的代码发送位置。
    原生的SocketMonitor不支持Http2.0

```
#### SocketMonitor对Http2.0的支持
    使用Q佬编译的文档： ...\session6\tools\socketmonitor.zip
    在 MonitorMode.java 程序中更新：
         private void check() 函数打开就能支持http2.0
         
#### 优点&局限性
```text
    对于SocketMonitor模块，可以⽆视掉证书的校验，直接获取到明⽂的数据，相⽐于中间⼈，不需要配
置代理就可以直接拿到抓包的数据。

    通过源码可以看到，这⾥监控了Java的Socket以及SSLSocket等相关类，因此对于直接在native层发起
的请求或者使⽤webview，这⾥是监控不到的，对于抓包这件事情，选择合适的⼯具，能完成需求就是
好的⽅案，不要局限于特定的⼯具。
```         

#### 使⽤⽅法
```text
    SocketMonitor.setPacketEventObserver(dataModel -> {
        try {
            //抓包数据在dataModel中，处理你的抓包业务即可
        } catch (Throwable throwable) {
            throwable.printStackTrace();
        }
    });

```
#### 使用实例
-  Hook-Code: ..\ratel01\app\src\main\java\com\example\ratel01\SocketMonitorEntry.java
```text

public class SocketMonitorEntry implements IRposedHookLoadPackage {
    private static final String TAG = "XXX";

    // 输入流（InputStream）转换为字符串的方法
    public String inputStreamToSting(InputStream inputStream) throws IOException {
        StringBuilder sb = new StringBuilder();
        for (int ch; (ch = inputStream.read()) != -1; ) {
            sb.append((char) ch);
        }
        return sb.toString();
    }


    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        // SocketMonitor的主要代码
        SocketMonitor.setPacketEventObserver(dataModel -> {
            try {
                // dataModel.data返回输入流
                Log.d(TAG, "onDecodeSocketData: "+ inputStreamToSting(dataModel.data));
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}

```


-  APP -Code: ..\CourseSix\app\src\main\java\com\yuanrenxue\course6\C17Activity.java
```text
    ---------------------------------------------------------------------------------
    public class C17Activity extends AppCompatActivity  implements View.OnClickListener {

    private EditText eturl;
    private Button ebtn;
    private final OkHttpClient client = new OkHttpClient.Builder().build();
    private static final String TAG = "jcak";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_c17);

        eturl = findViewById(R.id.send_url);
        ebtn = findViewById(R.id.bun);
        ebtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        String url = eturl.getText().toString();
        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                Log.d(TAG, "onFailure: 失败");
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                Log.d(TAG, "onResponse: "+ response.code());
            }
        });

    }
}

```