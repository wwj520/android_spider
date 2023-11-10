### 安装
   
     1.  pip install protobuf
     2. 下载proto编译器， 一个exe程序，把 proto.exe 加入到环境变量里
     https://github.com/protocolbuffers/protobuf/releases/
     D:\all_python_study\android_tools\protoc-24.3-win64\bin
### 手写一个Protobuf



### 序列化(正向开发)
- 流程：
```text
0. 写一个 Protobuf 文件，其中key不需要关心叫什么名字

1. proto.exe编译proto文件，自动生成python程序，生成的py文件会被引用
    protoc --python_out=. addressbook.proto
 
2. 生成.bin文件
    demo：protobug_正向开发.py
 
3. 利用proto.exe反解数据：反解得到的数据和接口返回的格式不一样，要还原
    protoc.exe --decode_raw < proto_data.bin
    返回结果deomo:
        1 {
          1: "wwj"
          2: 1
          3: "60@qq.com"
          4 {
            1: "18940967011"
          }
        }
        1 {
          1: "jack"
          2: 2
          3: "63216523@qq.com"
          4 {
            1: "18940967056"
          }
        }
  
4. 取值：
     ```python
     import addressbook_pb2
     address_book = addressbook_pb2.AddressBook()
     with open(r'proto_data.bin', "rb") as f:
        res = f.read()
        print(res)
        print(address_book.ParseFromString(res))
        print(address_book.people)
     ```
```

### 反序列化
 - 原因
    直接通过获取值，和 通过--decode_raw命令解析出的格式不一样，key值序列化后不存在


- 反解 Protobuf 方法一：
```text
0.将proto文件写入bin文件, 并使用 protoc.exe --decode_raw 反解
    // decode_raw可能报错
    // 遇到报错，直接报错抓包的response为xxx.bin文件

1.利用 protoc.exe 反解析 protobuf 数据
2.根据反解析出来的数据，还原出 .proto 文件
3.用 protoc.exe 编译 .proto 文件，生成 py 程序
4.用 py 程序可以轻松序列化和反序列化

```

- 反解 Protobuf 方法2：使用blackboxprotobuf步骤
```text
0. import blackboxprotobuf
1. 请求获取到proto文件后，保存到xx.bin文件中
2. 读取
      with open(r"xxx.bin", 'rb') as f:
        data = f.read()
        
    // protobuf_to_json：获取到json格式的
    messgae, message_type =blackboxprotobuf.protobuf_to_json(data, message_type=None)
    
    // decode_message： 获取到字典格式
    data_dict = blackboxprotobuf.decode_message(data)[0] 
    
    // 修改返回的结果：encode_message，这里的message_type 要用protobuf_to_json返回的
    data_dict['1']['2']['2'] = bytes("141路", encoding="utf-8")
    blackboxprotobuf.encode_message(data_dict, message_type=message_type)

```


