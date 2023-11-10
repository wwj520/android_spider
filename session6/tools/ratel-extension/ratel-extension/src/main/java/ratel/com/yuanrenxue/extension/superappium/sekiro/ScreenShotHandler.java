package ratel.com.yuanrenxue.extension.superappium.sekiro;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.view.Window;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.extension.superappium.ViewImage;
import com.virjar.ratel.api.extension.superappium.ViewImages;
import com.virjar.ratel.api.extension.superappium.traversor.Collector;
import com.virjar.ratel.api.extension.superappium.traversor.Evaluator;
import com.virjar.sekiro.business.api.interfaze.Action;
import com.virjar.sekiro.business.api.interfaze.AutoBind;
import com.virjar.sekiro.business.api.interfaze.RequestHandler;
import com.virjar.sekiro.business.api.interfaze.SekiroRequest;
import com.virjar.sekiro.business.api.interfaze.SekiroResponse;

import external.org.apache.commons.io.output.ByteArrayOutputStream;

import static com.virjar.sekiro.business.api.util.Constants.PAYLOAD_CONTENT_TYPE.PAYLOAD_CONTENT_TYPE;

@Action("screenShot")
public class ScreenShotHandler implements RequestHandler {

    @AutoBind
    private int quality = 50;

    @AutoBind
    private String viewHash;

    @AutoBind
    private String type = "activity";

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {
        Activity topActivity = PageTriggerManager.getTopActivity();
        if (topActivity == null) {
            sekiroResponse.failed("no data");
            return;
        }
        if (quality < 10) {
            quality = 10;
        } else if (quality > 100) {
            quality = 100;
        }
        PageTriggerManager.getMainLooperHandler().post(new Runnable() {

            private void screenShotInternal() {
                View decorView = null;

                if ("dialog".equalsIgnoreCase(type)) {
                    Window topDialogWindow = PageTriggerManager.getTopDialogWindow();
                    if (topDialogWindow != null) {
                        decorView = topDialogWindow.getDecorView();
                    }
                } else if ("popupWindow".equalsIgnoreCase(type)) {
                    decorView = PageTriggerManager.getTopPupWindowView();
                }

                if (decorView == null) {
                    decorView = PageTriggerManager.getTopRootView();
                }

                if (decorView == null) {
                    sekiroResponse.failed("no data");
                    return;
                }

                if (!TextUtils.isEmpty(viewHash)) {
                    ViewImages collect = Collector.collect(new Evaluator.ByHash(viewHash), new ViewImage(decorView));
                    if (collect.isEmpty()) {
                        sekiroResponse.failed("no data");
                        return;
                    }
                    decorView = collect.get(0).getOriginView();
                }

                if (decorView.getWidth() <= 0 || decorView.getHeight() <= 0) {
                    sekiroResponse.failed("zero img");
                    return;
                }

                Bitmap bitmap = Bitmap.createBitmap(decorView.getWidth(), decorView.getHeight(), Bitmap.Config.ARGB_8888);
                decorView.draw(new Canvas(bitmap));

                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.PNG, quality, byteArrayOutputStream);

                sekiroResponse.setHeader(PAYLOAD_CONTENT_TYPE, "image/png");
                sekiroResponse.send(byteArrayOutputStream.toByteArray());
            }


            @Override
            public void run() {
                try {
                    screenShotInternal();
                } catch (Throwable throwable) {
                    Log.e(SuperAppium.TAG, "screenShot failed", throwable);
                    sekiroResponse.failed(-1, throwable);
                }
            }
        });
    }
}