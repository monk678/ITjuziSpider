# -*- coding: utf-8 -*-
# @Time    : 2018年11月09日 4:17 PM
# @Author  : 李思原
# @Email   : shulisiyuan@163.com
# @File    : logoSpyder.py
# @Software: PyCharm
# @Describe: 保存logo图片.


import requests
import pymongo
import os

# mongodb链接信息
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dataSet"]
mycol = mydb["itjuziCompany"]
mycol = mydb["itjuziPersons"]


# 根据URL地址，文件名，文件存储路径下载文件
def saveFile(path, file_name, data):
    if data == None:
        return
    if not os.path.exists(path):
        os.makedirs(path)

    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


num = 0
for i in mycol.find():
    num += 1
    logoUrl = i['logo']
    companyId = i['id']
    companyName = i['name']
    # companyRegisterName = i['register_name']

    if logoUrl != 'https://cdn.itjuzi.com/assets/front/images/img/icon-person.png':
        print(num, companyName)

        data = requests.get(logoUrl).content
        saveFile(path='./imgSet/peason', file_name='%s_%s.jpg' % (companyName, companyId),
                  data=data)
