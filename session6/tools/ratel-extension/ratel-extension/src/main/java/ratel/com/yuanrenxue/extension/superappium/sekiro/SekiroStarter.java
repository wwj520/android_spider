package ratel.com.yuanrenxue.extension.superappium.sekiro;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.sekiro.business.api.SekiroClient;
import com.virjar.sekiro.business.api.interfaze.HandlerRegistry;
import com.virjar.sekiro.business.api.interfaze.SekiroRequest;
import com.virjar.sekiro.business.api.interfaze.SekiroRequestInitializer;

import java.util.UUID;

public class SekiroStarter {
    public static String sekiroGroup = "ratel-appium";

    private static boolean isStarted = false;

    private static SekiroClient defaultSekiroClient = null;

    public static void startService(String host, int port, String clientId) {
        if (isStarted) {
            return;
        }

        PageTriggerManager.getTopFragment("insureComponentStarted");
        defaultSekiroClient = new SekiroClient(sekiroGroup, clientId, host, port);
        defaultSekiroClient.setupSekiroRequestInitializer(new SekiroRequestInitializer() {
            @Override
            public void onSekiroRequest(SekiroRequest sekiroRequest, HandlerRegistry handlerRegistry) {
                handlerRegistry.registerSekiroHandler(new DumpTopActivityHandler());
                handlerRegistry.registerSekiroHandler(new DumpTopFragmentHandler());
                handlerRegistry.registerSekiroHandler(new ExecuteJsOnWebViewHandler());
                handlerRegistry.registerSekiroHandler(new FileExploreHandler());
                handlerRegistry.registerSekiroHandler(new ScreenShotHandler());
            }
        });
        defaultSekiroClient.start();

        isStarted = true;
    }

    public static void startService(String host, int port) {
        startService(host, port, UUID.randomUUID().toString());
    }

    public static SekiroClient getDefaultSekiroClient() {
        return defaultSekiroClient;
    }
}
