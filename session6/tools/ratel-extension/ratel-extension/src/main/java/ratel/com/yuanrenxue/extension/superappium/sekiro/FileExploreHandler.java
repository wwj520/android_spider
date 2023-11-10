package ratel.com.yuanrenxue.extension.superappium.sekiro;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.sekiro.business.api.interfaze.Action;
import com.virjar.sekiro.business.api.interfaze.AutoBind;
import com.virjar.sekiro.business.api.interfaze.RequestHandler;
import com.virjar.sekiro.business.api.interfaze.SekiroRequest;
import com.virjar.sekiro.business.api.interfaze.SekiroResponse;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import external.org.apache.commons.lang3.StringUtils;

@Action("fileExplore")
public class FileExploreHandler implements RequestHandler {

    @AutoBind(defaultValue = "/")
    private String path;

    @AutoBind(defaultValue = "get")
    private String op;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
        if (StringUtils.isBlank(path)) {
            path = "/";
        }
        String base = RatelToolKit.sContext.getFilesDir().getParentFile().getAbsolutePath();
        if (path.startsWith(base)) {
            path = path.substring(base.length());
        }
        File targetFile = new File(RatelToolKit.sContext.getFilesDir().getParent());
        if (!"/".equals(path)) {
            targetFile = new File(RatelToolKit.sContext.getFilesDir().getParentFile(), path);
        }


        if ("get".equalsIgnoreCase(op)) {
            if (!targetFile.exists()) {
                sekiroResponse.failed(404, "the file :" + targetFile.getAbsolutePath() + " not exist");
                return;
            }
            handleGet(sekiroRequest, sekiroResponse, targetFile);
        } else if ("post".equalsIgnoreCase(op)) {
            if (!targetFile.exists()) {
                sekiroResponse.failed(404, "the file :" + targetFile.getAbsolutePath() + " not exist");
                return;
            }
            handlePost(sekiroRequest, sekiroResponse, targetFile);
        } else if ("put".equalsIgnoreCase(op)) {
            handlePut(sekiroRequest, sekiroResponse, targetFile);
        } else if ("delete".equalsIgnoreCase(op)) {
            handleDelete(sekiroResponse, targetFile);
        }
    }

    private void handleDelete(SekiroResponse sekiroResponse, File targetFile) {
        if (!targetFile.isFile() || !targetFile.exists()) {
            sekiroResponse.failed("filed not exist");
        }
        if (targetFile.delete()) {
            sekiroResponse.success("success");
        } else {
            sekiroResponse.failed("remove failed");
        }

    }

    private void handleGet(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse, File targetFile) {
        if (targetFile.isDirectory()) {
            List<String> ret = new ArrayList<>();
            String[] list = targetFile.list();
            if (list == null) {
                sekiroResponse.failed("can not read dir file: " + targetFile.getAbsolutePath());
                return;
            }
            String base = RatelToolKit.sContext.getFilesDir().getParentFile().getAbsolutePath();
            for (String str : list) {
                if (str.startsWith(base)) {
                    ret.add(str.substring(base.length()));
                } else {
                    ret.add(str);
                }
            }
            sekiroResponse.success(ret);
            return;
        }
        if (!targetFile.canRead()) {
            sekiroResponse.failed("can not read file: " + targetFile.getAbsolutePath());
            return;
        }
        sekiroResponse.send(targetFile);
    }

    private void handlePost(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse, File targetFile) {
        sekiroResponse.failed("not implement now");
    }

    private void handlePut(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse, File targetFile) {
        sekiroResponse.failed("not implement now");
    }
}