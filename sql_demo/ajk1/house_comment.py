import csv
import re

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import pymysql
import pymongo

def Insert_Into_Mysql(goods,bads):
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
    data1["goods"] = goods
    data1["bads"] = bads
    # 执行INSERT语句，将数据插入到指定表中
    sql = "INSERT INTO house_comment(goods, bads) " \
          "VALUES (%s, %s)"
    val = (data1["goods"], data1["bads"])
    cursor.execute(sql, val)
    # 提交事务
    db1.commit()
    # 打印插入数据的行号
    print(cursor.rowcount, "记录插入成功。")
    # 关闭游标、MySQL连接
    cursor.close()
    db1.close()


def Insert_Into_MongoDB(goods,bads):
    # 连接到MongoDB数据库
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db2 = client["ajk_house"]
    collection = db2["house_3"]
    # 获取需要写入MongoDB的数据
    data2 = {}
    # 写入mongoDB数据库
    data2['goods'] = goods
    data2['bads'] = bads
    # 将数据插入到MongoDB集合中
    x = collection.insert_one(data2)
    # 打印插入数据的ObjectId
    print(x.inserted_id)
    # 关闭mongoDB数据库连接
    client.close()

def get_comment(url, f2, f3, log):
    try:
        web = Chrome()
        web.get(url)
        web.maximize_window()
        time.sleep(5)
        try:
            iframe = web.find_element(By.XPATH, '//*[@id="iframeLoginIfm"]')
            web.switch_to.frame(iframe)
            login = web.find_element(By.XPATH, '//*[@id="pwdTab"]')
            login.click()
            time.sleep(5)
            # 输入账号
            username = web.find_element(By.XPATH, '//*[@id="pwdUserNameIpt"]')
            username.send_keys("15738108003")
            time.sleep(5)
            # 输入密码
            password = web.find_element(By.XPATH, '//*[@id="pwdIpt"]')
            password.send_keys("Wyz666666")
            time.sleep(5)
            # 同意用户协议
            checkagreen = web.find_element(By.XPATH, '//*[@id="checkagree"]')
            checkagreen.click()
            time.sleep(10)
            # 找到登录按钮，并点击
            submit_btn = web.find_element(By.XPATH, '//*[@id="pwdSubmitBtn"]')
            submit_btn.click()
            time.sleep(5)
        except:
            pass
        time
        advantage = web.find_elements(By.XPATH, '/html/body/div[2]/div[6]/ul/li')
        for i in advantage:
            goods=i.find_element(By.XPATH, './div[2]/dl[1]').text
            goods = re.sub(",", "，", goods)
            print(goods)
            bads =i.find_element(By.XPATH, './div[2]/dl[2]').text
            bads = re.sub(",", "，", bads)
            print(bads)
            f2.write(f"{goods}\n")
            f3.write(f"{bads}\n")
            # mongoDB数据库 - 数据持久化
            Insert_Into_MongoDB(goods,bads)
            # mysql数据库 - 数据持久化
            Insert_Into_Mysql(goods,bads)
        web.refresh()
    except Exception as e:
        log.write(f"{url}\n")
        print(e)


if __name__ == '__main__':
    f2 = open("./data/advantage1.csv", mode="a", encoding="utf-8")
    f3 = open("./data/disadvantage1.csv", mode="a", encoding="utf-8")
    log = open("./data/comment_log.csv", mode="a", encoding="utf-8")
    log.write("url\n")
    with open("E:\\大三下\\爬虫\\qimo\\sql_demo\\ajk1\\data\\zz_house_detail.csv", 'r',
              encoding="utf-8") as file:
        reader = csv.reader(file)
        # 跳过文件的第一行
        next(reader)
        # 读取文件中的URL地址
        for row in reversed(list(reader)):
            url = row[8]
            get_comment(url, f2, f3, log)
    f2.close()
    f3.close()
    log.close()
