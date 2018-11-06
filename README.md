# ITjuziSpider

本程序爬取IT桔子https://www.itjuzi.com 的4个部分：


1：公司/项目 （itjuziCompanySpider.py）

2：投融资速递 （itjuziInvesteventSpider.py）

3：投资机构 （itjuziInvestmentsSpider.py）

4：创投人物 （itjuziPersonsSpider.py）


本爬虫爬到数据后，插入MongoDB中。
安装好相关的依赖包后，
 1：requests
 
 2：pymongo
 
 3：json
 
 4：time
 
 5：random
 
 6：string
 
 7：configparser

运行方法：直接运行对应的py文件即可开始爬虫。
注意：IT桔子有VIP账号校验，因此，你需要购买VIP，将你的账号，密码写入config.ini文件中

爬虫方法，请查看我的博客：www.siyuanblog.com
