### So动态库的加载流程
```text
dlopen -> CallConstructors -> init，init_array(反调试，检测，ollvm字符串加解密)
dlsym(JNI_ONLOAD)
```
  