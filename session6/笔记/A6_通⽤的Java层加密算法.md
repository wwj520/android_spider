## Java密码/编码相关知识
- Java 字节(Byte) 取值范围 [-128,127]；Python3 字节(bytes) 取值范围： [0,256)

- 字节数组 / HEX字符串 / Base64 编码之间的关系：
```jupyter

1. 字节数组转换为十六进制字符串：
public static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
        sb.append(String.format("%02x", b));
    }
    return sb.toString();
}
 
2. 十六进制字符串转换为字节数组：
public static byte[] hexToBytes(String hex) {
    int len = hex.length();
    byte[] bytes = new byte[len / 2];
    for (int i = 0; i < len; i += 2) {
        bytes[i / 2] = (byte) ((Character.digit(hex.charAt(i), 16) << 4)
                             + Character.digit(hex.charAt(i + 1), 16));
    }
    return bytes;
}
3. 字节数组转换为Base64编码：
import java.util.Base64;

public static String bytesToBase64(byte[] bytes) {
    return Base64.getEncoder().encodeToString(bytes);
}

4. Base64编码转换为字节数组：
import java.util.Base64;

public static byte[] base64ToBytes(String base64) {
    return Base64.getDecoder().decode(base64);
}

```

## AES/DES/MD5/SH1 加解密实例
```jupyter
public class CryptoUtils implements ICryptoUtils {
    @Override
    public String aesEncrypt(String key, String iv, String content) throws Exception {
        // key.getBytes(): 获取字节数组
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), "AES");
        // iv
        IvParameterSpec ivSpec = new IvParameterSpec(iv.getBytes());
        // 构造算法
        // 获取到加密实例
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        // 加密算法初始化
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, ivSpec);
        byte[] bytes = cipher.doFinal(content.getBytes());
        return Base64.encodeToString(bytes, Base64.DEFAULT);
    }

    @Override
    public String aesDecrypt(String key, String iv, String content) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(iv.getBytes());

        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        // 解密算法初始化
        cipher.init(Cipher.DECRYPT_MODE, keySpec, ivSpec);
        //content:需要将base64转换为字节数组
        byte[] bytes = cipher.doFinal(Base64.decode(content, Base64.DEFAULT));
        // 界面需要字节转字符串：new String(bytes)
        return new String(bytes);

    }

    @Override
    public String desEncrypt(String key, String content) throws Exception {
        // key.getBytes(): 获取字节数组
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), "DES");
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        // 算法初始化
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        byte[] bytes = cipher.doFinal(content.getBytes());
        return Base64.encodeToString(bytes, Base64.DEFAULT);
    }

    @Override
    public String desDecrypt(String key, String content) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), "DES");
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, keySpec);
        byte[] bytes = cipher.doFinal(Base64.decode(content, Base64.DEFAULT));
        return new String(bytes);
    }

    /*
    以下是哈希函数
    */
    @Override
    public String getMD5(String content) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        // 返回字节数组，
        // digest之前要分块调用 update方法，进源码中查看
        byte[] bytes = md.digest(content.getBytes());
        // 字节数组转为16进制字符串
        return new BigInteger(1, bytes).toString(16);

    }

    @Override
    public String getSHA1(String content) throws Exception {
        MessageDigest sha1 = MessageDigest.getInstance("SHA1");
        byte[] bytes = sha1.digest(content.getBytes());
        return new BigInteger(1, bytes).toString(16);
    }
}

```


## HOOK 加密/解密 过程中的各个节点

     位置：D:\AndroidStudioProjects\ratel01\app\src\main\java\com\example\ratel01\HookCrypto.java
- 代码
```jupyter
public class HookCrypto implements IRposedHookLoadPackage {
    private static final String TAG = "yuanrenxue----------";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.yuanrenxue.course6")){

            //1. hook-AES密钥：new SecretKeySpec(key.getBytes(), "AES");
            // 这里不用写包名+反射，而是直接写SecretKeySpec.class是因为 SecretKeySpec是java的类
            RposedHelpers.findAndHookConstructor(SecretKeySpec.class, byte[].class, String.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    // param.args[0]是一个object，要进行强制类型转换
                    Log.d(TAG, String.format("SecretKeySpec(%s,%s)", new String((byte[]) param.args[0]),param.args[1]));

                }
            });

            // 2. hook new IvParameterSpec(iv.getBytes());
            RposedHelpers.findAndHookConstructor(IvParameterSpec.class, byte[].class, new RC_MethodHook() {
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    Log.d(TAG, String.format("IvParameterSpec(%s)", new String((byte[]) param.args[0])));

                }
            });

            //3. hook 采用了什么加密算法： Cipher.getInstance()
            RposedHelpers.findAndHookMethod(Cipher.class, "getInstance", String.class, new RC_MethodHook() {
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    Log.d(TAG, "采用的加密算法：" + param.args[0]);
                }
            });

            //4.hook 加密解密： cipher.doFinal
            RposedHelpers.findAndHookMethod(Cipher.class, "doFinal", byte[].class, new RC_MethodHook() {
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    // param.getResult() 返回的是一个 Object 类型的对象，入参和返回值都是要返回字节数组，都要做强制类型转换(byte[])
                    Log.d(TAG, String.format("入参%s, 返回值：%s", new String((byte[]) param.args[0]), new String((byte[])param.getResult())));
                }
            });

        }
    }
}
```


