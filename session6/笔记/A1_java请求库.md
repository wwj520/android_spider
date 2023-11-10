#### 步骤
1.  在AndroidManifest.xml添加网络权限
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.example.myapplication2">
    <uses-permission android:name="android.permission.INTERNET"/>
</manifest>
```

#### OKhttp
- https://square.github.io/okhttp/
- demo
```java
package com.example.myapplication2;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.io.IOException;
import java.text.Format;
import java.util.logging.Handler;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import retrofit2.http.HTTP;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private final OkHttpClient client = new OkHttpClient.Builder()
            .addInterceptor(new LogingInterceptor())
            .build();
    private static  final String TAG = "curry";
    private TextView tvContent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findViewById(R.id.btn_test).setOnClickListener(this);
        tvContent = findViewById(R.id.tv_content);
    }

    @Override
    public void onClick(View v){
        okhttpPost();
    }


    // 同步： client.newCall(request).execute()
    void okhttpDemo() {

        Request request = new Request.Builder().url("https://reqres.in/api/users?page=2").build();
        tvContent.setText("请求中......");
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Response response = client.newCall(request).execute();
                    Log.d(TAG, "okhttpDemo:"+response.body().string());
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            tvContent.setText("状态码："+response.code());
                        }
                    });
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        }).start();

    }

    // 异步get请求：  client.newCall(request).enqueue
    void okhttpAsyncDemo(){
        tvContent.setText("******************");
        Request request = new Request.Builder().url("https://reqres.in/api/users?page=2").build();
        tvContent.setText("请求中......");

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                Log.d(TAG, "请求失败");
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                Log.d(TAG, "okhttpDemo:"+response.body().string());
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        tvContent.setText("状态码："+response.code());
                    }
                });
            }
        });

    }

    // 构建get请求参数
    void okhttpParms(){
        HttpUrl.Builder builder =  HttpUrl.parse("https://reqres.in/api/users").newBuilder();
        builder.addQueryParameter("page", "3");
        String url = builder.build().toString();
        Log.d(TAG, "okhttpParm: "+url);
    }

    // 构建post请求
    void okhttpPost(){
        RequestBody body = new FormBody.Builder()
                .add("name", "wwj")
                .add("job", "xxx")
                .build();

        Request request = new Request.Builder().url("https://reqres.in/api/users")
                .post(body)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                Log.d(TAG, "请求失败");
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                Log.d(TAG, "okhttpPost:"+response.body().string());
            }
        });
    }

}
```



#### retrofit
- 对okhttp3进⾏了⼀个封装, 是⼀个类型安全的http客户端
-  https://square.github.io/retrofit/
- demo 
```java
    // retrofit-GET
    void retrofitGetDemo(){
        tvContent.setText("请求中");
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://reqres.in/")
                //转化器：将json结果序列化为java对象
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        retrofit.create(retrofitApiService.class).listUsers(2).enqueue(new retrofit2.Callback<retrofitPersonFormat>() {
            @Override
            public void onResponse(retrofit2.Call<retrofitPersonFormat> call, retrofit2.Response<retrofitPersonFormat> response) {
                Log.d(TAG, "retrofitGetDemo:" +response.body());
                tvContent.setText("请求状态码：" + response.code());
            }

            @Override
            public void onFailure(retrofit2.Call<retrofitPersonFormat> call, Throwable t) {
                Log.d(TAG, "retrofitGetError:" +t.toString());
            }
        });

    }


    // retrofit-post
    void retrofitPostDemo(){
        tvContent.setText("请求中");
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://reqres.in/")
                //转化器：将json结果序列化为java对象
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        retrofit.create(retrofitApiService.class).createUser("WWJ", "police").enqueue(new retrofit2.Callback<UserBean>() {
            @Override
            public void onResponse(retrofit2.Call<UserBean> call, retrofit2.Response<UserBean> response) {
                Log.d(TAG, "retrofiPostDemo:" +response.body().toString());
                Log.d(TAG, "retrofiPostDemo:" +response.body().name);
                tvContent.setText("请求状态码：" + response.code());
            }

            @Override
            public void onFailure(retrofit2.Call<UserBean> call, Throwable t) {
                Log.d(TAG, "retrofitPostError:" +t.toString());
            }
        });

    }





```


#### rxjava
- https://github.com/ReactiveX/RxJava
- 注意：请求中需要自行切换进程
```javascript
 void rxjavaGetDemo() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://reqres.in/")
                //转化器：将json结果序列化为java对象
                .addConverterFactory(GsonConverterFactory.create())
                // 添加 rxjava支持
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .build();

        retrofit.create(retrofitApiService.class).rxListUsers(2)
                // rxjava需要自己将请求放入子线程
                .subscribeOn(Schedulers.io())
                // 切换回主线程
                .observeOn(AndroidSchedulers.mainThread())
                // 注册
                .subscribe(new Observer<retrofitPersonFormat>() {
                    @Override
                    public void onSubscribe(Disposable disposable) {
                        tvContent.setText("请求中...");
                    }

                    @Override
                    public void onNext(retrofitPersonFormat retrofitPersonFormat) {
                        Log.d(TAG, "onNext:" + retrofitPersonFormat.totalPage);

                    }

                    @Override
                    public void onError(Throwable throwable) {
                        throwable.printStackTrace();
                    }

                    @Override
                    public void onComplete() {
                        tvContent.setText("请求完成");
                    }
                });

    }



```


