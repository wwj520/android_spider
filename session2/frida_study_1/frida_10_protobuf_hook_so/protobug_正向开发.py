# -*- coding:utf-8 -*-
from session2.frida_study_1.frida_10_protobuf_hook_so import addressbook_pb2


def PromptForAddress(person):
    person.id = int(input("Enter person ID number: "))
    person.name = input("Enter name: ")

    email = input("Enter email address (blank for none): ")
    if email != "":
        person.email = email

    while True:
        number = input("Enter a phone number (or leave blank to finish): ")
        if number == "":
            break

        phone_number = person.phones.add()
        phone_number.number = number

        type = input("Is this a mobile, home, or work phone? ")
        if type == "mobile":
            phone_number.type = addressbook_pb2.Person.MOBILE
        elif type == "home":
            phone_number.type = addressbook_pb2.Person.HOME
        elif type == "work":
            phone_number.type = addressbook_pb2.Person.WORK
        else:
            print("Unknown phone type; leaving as default value.")


address_book = addressbook_pb2.AddressBook()

PromptForAddress(address_book.people.add())
PromptForAddress(address_book.people.add())

# Write the new address book back to disk.
with open(r'D:\all_python_study\yuanrenxue_android_code\session2\frida_study_1\frida_10_protobuf_hook_so\proto_data.bin', "wb") as f:
    f.write(address_book.SerializeToString())

