import requests
import pymongo
import json
import time
import random
import string
from configparser import ConfigParser

config = ConfigParser()
config.readfp(open('config.ini'))
userName = config.get("userInfo", "userName")
passWord = config.get("userInfo", "passWord")

url = config.get("spiderAPI", "companySpider")

# mongodb链接信息
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dataSet"]
mycol = mydb["itjuziCompany"]


# 一个初始的headers
headers0 = {
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    'Authorization': "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3d3dy5pdGp1emkuY29tL2FwaS9hdXRob3JpemF0aW9ucyIsImlhdCI6MTU0MTA2MjgyMiwiZXhwIjoxNTQxMDcwMDIyLCJuYmYiOjE1NDEwNjI4MjIsImp0aSI6ImZxNThmd2pmQzUwSmVPa0EiLCJzdWIiOjY1NzkwNSwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.hj6iFzfBKO3mVgNaZi4LMIkIx1pBXDAhxoPrRqnZu-M",
    'Connection': "keep-alive",
    'Content-Length': "146",
    'Content-Type': "application/json;charset=UTF-8",
    'Cookie': "acw_tc=781bad0815402688023056452e7c576c41045e5b29de9a4b3f36068143759e; _ga=GA1.2.1517124744.1540268810; gr_user_id=952fbb1b-5651-4cb4-b87d-2849b63d24d8; MEIQIA_EXTRA_TRACK_ID=1BxdnZcwNabrjlxmOJNiI668Zpr; identity=15201733273%40test.com; unique_token=657905; MEIQIA_VISIT_ID=1CKSDWVxqoJCEJPWlT82cOjr1Gv; remember_code=km7Th.O1Co; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1540881921,1540966674,1540966886,1540967676; session=8557017237becf774165f5b7cfd7dd3056ba492a; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1540968165",
    'Host': "www.itjuzi.com",
    'Origin': "https://www.itjuzi.com",
    'Referer': "https://www.itjuzi.com/company",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}


# 动态生成headers，首先随机生成一个62位的cookie值，再使用这个随机字符串掉接口生成认证码，最后包装成headers
def getHeaders():
    url = "https://www.itjuzi.com/api/authorizations"
    cookie = ''.join(random.sample(string.ascii_letters + string.digits, 62))

    payload = "{\"account\":\"%s\",\"password\":\"%s\"}" % (userName, passWord)
    headers = {
        'Host': "www.itjuzi.com",
        'Connection': "keep-alive",
        'Content-Length': "51",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://www.itjuzi.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Content-Type': "application/json;charset=UTF-8",
        'Referer': "https://www.itjuzi.com/login?url=%2Fcompany",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "acw_tc=%s" % cookie
    }

    response = requests.request("POST", url, data=payload, headers=headers).text
    response = json.loads(response)

    token = response['data']['token']
    headers = {
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        'Authorization': "%s" % token,
        'Connection': "keep-alive",
        'Content-Length': "146",
        'Content-Type': "application/json;charset=UTF-8",
        'Cookie': "acw_tc=%s;" % cookie,
        'Host': "www.itjuzi.com",
        'Origin': "https://www.itjuzi.com",
        'Referer': "https://www.itjuzi.com/company",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    return headers


headers0 = getHeaders()


# 爬虫主体
def getInfoByPageNum(pageNum, headers=headers0):
    payload = "{\"pagetotal\":116953,\"total\":0,\"per_page\":20,\"page\":%s,\"scope\":\"\",\"sub_scope\":\"\",\"round\":\"\",\"prov\":\"\",\"city\":\"\",\"status\":\"\",\"sort\":\"\",\"selected\":\"\"}" % pageNum
    try:
        # headers = getHeaders()
        response = requests.request("POST", url, data=payload, headers=headers)
        data = response.text.replace('\n', '')
        print(data)
        print(headers['Cookie'])
        rows = json.loads(data)['data']['data']

        if json.loads(data)['status'] != 'success':
            print('遇到了反爬虫1，休息10秒')
            time.sleep(10 + random.random() * 5)
            headers = getHeaders()
            getInfoByPageNum(pageNum=pageNum, headers=headers)

        totalPage = int(json.loads(data)['data']['page']['total'])
        pageNumNow = int(json.loads(data)['data']['page']['page'])

        return totalPage, pageNumNow, rows
    except requests.exceptions.ConnectionError:
        print('遇到了反爬虫2，休息10秒')
        headers = getHeaders()
        time.sleep(10 + random.random() * 5)
        headers = getHeaders()
        getInfoByPageNum(pageNum=pageNum, headers=headers)

    except KeyError:
        print('遇到了反爬虫3，休息10秒,重新生成headers')
        headers = getHeaders()
        print('》》》', headers['Cookie'])
        # time.sleep(10 + random.random() * 5)
        getInfoByPageNum(pageNum=pageNum, headers=headers)


# 插入到MongoDB
def insertToMongo(rows):
    if rows:
        for row in rows:
            row['spider_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            try:
                mycol.insert_one(row)
                # print(row)
            except:
                # print('>>>>>>:', row, '已经存在')
                pass


if __name__ == '__main__':
    pageNumNow = 1
    totalPage, pageNumNow, rows = getInfoByPageNum(pageNum=pageNumNow)
    print('一共有：%s页' % totalPage)
    print('正在爬取第%s/%s页' % (pageNumNow, totalPage))
    while pageNumNow <= totalPage:
        # insertToMongo(rows=rows)
        try:
            totalPage, pageNumNow, rows = getInfoByPageNum(pageNum=pageNumNow + 1)
            print('正在爬取第%s/%s页' % (pageNumNow + 1, totalPage))
        except TypeError as e:
            pass
            print(e)
        # time.sleep(1 + 2 * random.random())
    else:
        print('爬虫结束')
