# -*- coding:utf-8 -*-
from session2.frida_study_1.frida_10_protobuf_hook_so import addressbook_pb2

# address_book = addressbook_pb2.AddressBook()
address_book = addressbook_pb2.AddressBook()


# Write the new address book back to disk.
with open(r'D:\all_python_study\yuanrenxue_android_code\session2\frida_study\frida_10_protobuf_hook_so\proto_data.bin', "rb") as f:
    res = f.read()
    print(res)
    print(address_book.ParseFromString(res))
    print(address_book.people)



