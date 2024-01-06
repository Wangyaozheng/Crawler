import csv
import re

import pymysql
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

import pymysql
import pymongo
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

# # 随机选择一个代理IP地址
# proxies = [
#     "https://n364.kdltps.com:15818",
# ]
# proxy = Proxy()
# proxy.proxy_type = ProxyType.MANUAL
# proxy.http_proxy = random.choice(proxies)
# proxy.ssl_proxy = random.choice(proxies)
#
# options = webdriver.ChromeOptions()
# options.add_argument("--proxy-server={}".format(proxy.http_proxy))


def Insert_Into_Mysql(Decoration,Ownership_Type,Property_Type,periods,budget,Company,License,points):
    # 连接到MySQL数据库
    db1 = pymysql.connect(
        host="localhost",
        user="abc",
        password="123456",
        database="ajk_house"
    )
    # 获取游标
    cursor = db1.cursor()
    # 获取需要写入MongoDB的数据
    data1 = {}
    # 获取游标
    cursor = db1.cursor()
    data1["Decoration"] = Decoration
    data1["Ownership_Type"] = Ownership_Type
    data1["Property_Type"] = Property_Type
    data1["periods"] = periods
    data1["budget"] = budget
    data1["Company"] = Company
    data1["License"] = License
    data1["points"] = points
    # 执行INSERT语句，将数据插入到指定表中
    sql = "INSERT INTO house_detail(Decoration, Ownership_Type, Property_Type,periods,budget, Company, License,points) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (data1["Decoration"], data1["Ownership_Type"], data1["Property_Type"], data1['periods'],data1["budget"], data1["Company"],
           data1["License"], data1["points"])
    cursor.execute(sql, val)
    # 提交事务
    db1.commit()
    # 打印插入数据的行号
    print(cursor.rowcount, "记录插入成功。")
    # 关闭游标、MySQL连接
    cursor.close()
    db1.close()


def Insert_Into_MongoDB(Decoration,Ownership_Type,Property_Type,periods,budget,Company,License,points):
    # 连接到MongoDB数据库
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db2 = client["ajk_house"]
    collection = db2["house_2"]
    # 获取需要写入MongoDB的数据
    data2 = {}
    # 写入mongoDB数据库
    data2["Decoration"] = Decoration
    data2["Ownership_Type"] = Ownership_Type
    data2["Property_Type"] = Property_Type
    data2["periods"] = periods
    data2["budget"] = budget
    data2["Company"] = Company
    data2["License"] = License
    data2["points"] = points
    # 将数据插入到MongoDB集合中
    x = collection.insert_one(data2)
    # 打印插入数据的ObjectId
    print(x.inserted_id)
    # 关闭mongoDB数据库连接
    client.close()


def get(url, f1, log):
    try:
        web = Chrome()
        web.get(url)
        print(url)
        web.maximize_window()
        time.sleep(15)
        Decoration = web.find_element(By.XPATH,'//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]')
        Decoration = Decoration.text
        time.sleep(5)
        # scroll_distance = 50
        # web.execute_script("window.scrollTo(0, document.body.scrollHeight-{0});".format(scroll_distance))产权性质，物业类型，产权年限，唯一住房，发布公司，核心卖点
        if web.page_source.find('>产权性质</span>') != -1:
            Ownership_Type = web.find_element(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr[1]/td[2]/span[2]')
            Ownership_Type = Ownership_Type.text
        else:
            Ownership_Type = "NAN"
        time.sleep(5)
        if web.page_source.find('>物业类型</span>') != -1:
            Property_Type = web.find_element(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr[1]/td[3]/span[2]')
            Property_Type = Property_Type.text
        else:
            Property_Type = "NAN"
        time.sleep(5)
        if web.page_source.find('>产权年限</span>') != -1:
            periods = web.find_element(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr[2]/td[2]/span[2]')
            periods = periods.text
        else:
            periods = "NAN"
        time.sleep(5)
        if web.page_source.find('>唯一住房</span>') != -1:
            budget = web.find_element(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr[4]/td[2]/span[2]')
            budget = budget.text
        elif web.page_source.find('>唯一住房</span>') == -1:
            budget = web.find_element(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr[3]/td[2]/span[2]')
            budget = budget.text
        else:
            budget = "NAN"
        time.sleep(5)
        if web.page_source.find('>发布公司</span>') != -1:
            Company = web.find_elements(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr')[-2]
            Company = Company.find_element(By.XPATH, './td[2]/span[2]')
            Company = Company.text
        else:
            Company = "NAN"
        time.sleep(5)
        if web.page_source.find('>营业执照</span>') != -1:
            License = web.find_elements(By.XPATH, '//*[@id="houseInfo"]/table/tbody/tr')[-1]
            License = License.find_element(By.XPATH, './td[2]/span[2]')
            License = License.text
        else:
            License = "NAN"
        time.sleep(5)
        if web.page_source.find('>核心卖点</span>') != -1:
            element = web.find_element(By.XPATH, '//*[@id="houseIntro"]/div[2]/div/div/div[2]/div[2]/div')
            points = element.text
            # 替换<br>标签为空格
            points = re.sub("\n", "", points)
            points = re.sub(",", "，", points)
        else:
            points = "NAN"
        time.sleep(5)
        if web.page_source.find('>查看更多经纪人解读') != -1:
            Comment_url = web.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[1]/div[7]/div[1]/a')
            Comment_url = Comment_url.get_attribute("href")
        else:
            Comment_url = ''
        time.sleep(5)
        print(
            f"{Decoration},{Ownership_Type},{Property_Type},{periods},{budget},{Company},{License},{points},{Comment_url}\n")
        # 写入 csv文件
        f1.write(
            f"{Decoration},{Ownership_Type},{Property_Type},{periods},{budget},{Company},{License},{points},{Comment_url}\n")
        # mongoDB数据库 - 数据持久化
        Insert_Into_MongoDB(Decoration,Ownership_Type,Property_Type,periods,budget,Company,License,points)
        # mysql数据库 - 数据持久化
        Insert_Into_Mysql(Decoration,Ownership_Type,Property_Type,periods,budget,Company,License,points)
    except Exception as e:
        log.write(f"{url}\n")
        print(e)
    time.sleep(15)
    web.close()


if __name__ == '__main__':
    urls = []
    f1 = open("./data/zz_house_detail3.csv", mode="a", encoding="utf-8")
    log = open("./data/log.csv", mode="w", encoding="utf-8")
    f1.write("Decoration,Ownership_Type,Property_Type,periods,budget,Company,License,points,Comment_url\n")
    log.write("url\n")
    with open("E:\\大三下\\爬虫\\qimo\\sql_demo\\ajk1\\data\\zz_houseinfo.csv", 'r',
              encoding="utf-8") as file:
        reader = csv.reader(file)
        # 跳过文件的第一行
        next(reader)
        # 读取文件中的URL地址
        for row in reversed(list(reader)):
            url = row[10]
            get(url, f1, log)
    f1.close()
    log.close()
