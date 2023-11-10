package ratel.com.yuanrenxue.extension.superappium.sekiro;

import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.webkit.ValueCallback;
import android.webkit.WebView;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.extension.superappium.ViewImage;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.business.api.fastjson.JSON;
import com.virjar.sekiro.business.api.fastjson.JSONObject;
import com.virjar.sekiro.business.api.interfaze.Action;
import com.virjar.sekiro.business.api.interfaze.AutoBind;
import com.virjar.sekiro.business.api.interfaze.RequestHandler;
import com.virjar.sekiro.business.api.interfaze.SekiroRequest;
import com.virjar.sekiro.business.api.interfaze.SekiroResponse;

import static com.virjar.sekiro.business.api.util.Constants.PAYLOAD_CONTENT_TYPE.PAYLOAD_CONTENT_TYPE;


@Action("executeJs")
public class ExecuteJsOnWebViewHandler implements RequestHandler {
    @AutoBind
    private String jsCode;

    @AutoBind
    private String type = "activity";


    @Override
    public void handleRequest(final SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {

        PageTriggerManager.getMainLooperHandler().post(new Runnable() {

            private void dumpInternal() {
                View topRootView = null;

                if ("dialog".equalsIgnoreCase(type)) {
                    Window topDialogWindow = PageTriggerManager.getTopDialogWindow();
                    if (topDialogWindow != null) {
                        topRootView = topDialogWindow.getDecorView();
                    }
                } else if ("popupWindow".equalsIgnoreCase(type)) {
                    topRootView = PageTriggerManager.getTopPupWindowView();
                }

                if (topRootView == null) {
                    topRootView = PageTriggerManager.getTopRootView();
                }


                if (topRootView == null) {
                    sekiroResponse.failed("no topRootView found");
                    return;
                }

                ViewImage viewImage = new ViewImage(topRootView);
                final WebView webView = viewImage.findWebViewIfExist();
                if (webView == null) {
                    sekiroResponse.failed("no WebView found");
                    return;
                }
                new Handler((Looper) RposedHelpers.getObjectField(webView, "mWebViewThread")).post(new Runnable() {
                    @Override
                    public void run() {
                        //android.webkit.WebView#evaluateJavascript(String script, @RecentlyNullable ValueCallback<String> resultCallback) {
                        RposedHelpers.callMethod(webView, "evaluateJavascript", jsCode, new ValueCallback<String>() {
                            @Override
                            public void onReceiveValue(String s) {
                                JSONObject jsonObject = JSON.parseObject("{\"data\":" + s + "}");
                                String data = jsonObject.getString("data");
                                if (data == null) {
                                    data = "undefined";
                                }
                                sekiroResponse.setHeader(PAYLOAD_CONTENT_TYPE, "text/html");
                                sekiroResponse.send(data);
                            }
                        });
                    }
                });

            }


            @Override
            public void run() {
                try {
                    dumpInternal();
                } catch (Exception e) {
                    sekiroResponse.failed(-1, e);
                    Log.w(SuperAppium.TAG, "dump activity error", e);
                }
            }
        });
    }
}