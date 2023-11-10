# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/8/23
# description: 请求参数signature  python还原
import hashlib

strs = "IMEI867686021254857-IMSI460NNNNNNNNNNNN&&1693302361&&f1190aca-d08e-4041-8666-29931cd89dde"
sig = ""
instance = hashlib.md5()
instance.update(bytearray(strs.encode('utf8')))
digest = instance.digest()
for b2 in digest:
    # format 可用于指定进制转化
    """
    format(x,'b')         #将x转换为二进制
    format(x,'o')         #将x转换为八进制
    format(x,'d')         #将x转换为十进制
    format(x,'x')         #将x转换为十六进制
    """
    sig += format((b2 >> 4) & 15, 'x')+format(b2 & 15, "x")
print(sig)