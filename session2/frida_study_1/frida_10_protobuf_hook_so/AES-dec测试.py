# -*- coding:utf-8 -*-
# author:jackwu 
# time:2023/9/11
# description:
import binascii

from Crypto.Cipher import AES

key = '2fd3028e14a45d1f8b6eb0b2adb7caaf'
iv = '754c8fd584facf6210376b2b72b063e4'
aes = AES.new(binascii.a2b_hex(key), AES.MODE_CBC, binascii.a2b_hex(iv))
content = "be4978de5bb680a11a84d6663664c479bc0617040c81cfe0c258bf7e218c0cf1b760c16f157d4829856212b781ca03e36a4d9b73f47c1f6d3676b05ca9d407556061fe0e166c9ab53e5a71e12ca86d642ce26e244e67d512b526cff11bd0ad3e669f23ac713ba86da80f2a07370a52d2"

# binascii.a2b_hex:返回由十六进制字符串十六进制表示的二进制数据
dec = aes.decrypt(binascii.a2b_hex(content))
print(dec)