import re
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import pymysql
import pymongo


def Insert_Into_Mysql(title, unitType, size, Chaoxiang, floor, nianfen, Community, address, price, unitPrice):
    # 连接到MySQL数据库
    db1 = pymysql.connect(
        host="localhost",
        user="abc",
        password="123456",
        database="ajk_house"
    )
    # 获取游标
    cursor = db1.cursor()
    data1 = {}
    # 获取游标
    cursor = db1.cursor()
    data1["title"] = title
    data1["unitType"] = unitType
    data1["size"] = size
    data1["Chaoxiang"] = Chaoxiang
    data1["floor"] = floor
    data1["nianfen"] = nianfen
    data1["Community"] = Community
    data1["address"] = address
    data1["price"] = price
    data1["unitPrice"] = unitPrice
    # 执行INSERT语句，将数据插入到指定表中 标题，户型，面积，朝向，楼层，年份，小区，地址，总价，单价。
    sql = "INSERT INTO house(title, unitType, size, Chaoxiang, floor, nianfen, Community, address, price, unitPrice) " \
          "VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (data1["title"], data1["unitType"], data1["size"], data1["Chaoxiang"], data1["floor"],
           data1["nianfen"], data1["Community"], data1["address"], data1["price"], data1["unitPrice"])
    cursor.execute(sql, val)
    # 提交事务
    db1.commit()
    # 打印插入数据的行号
    print(cursor.rowcount, "记录插入成功。")
    # 关闭游标、MySQL连接
    cursor.close()
    db1.close()


def Insert_Into_MongoDB(title, unitType, size, Chaoxiang, floor, nianfen, Community, address, price, unitPrice):
    # 连接到MongoDB数据库
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db2 = client["ajk_house"]
    collection = db2["house_4"]
    # 获取需要写入MongoDB的数据
    data2 = {}
    # 写入mongoDB数据库
    data2["title"] = title
    data2["unitType"] = unitType
    data2["size"] = size
    data2["Chaoxiang"] = Chaoxiang
    data2["floor"] = floor
    data2["nianfen"] = nianfen
    data2["Community"] = Community
    data2["address"] = address
    data2["price"] = price
    data2["unitPrice"] = unitPrice
    # 将数据插入到MongoDB集合中
    x = collection.insert_one(data2)
    # 打印插入数据的ObjectId
    print(x.inserted_id)
    # 关闭mongoDB数据库连接
    client.close()


def getInfo(url, f, log):
    try:
        web = Chrome()
        web.get(url)
        web.maximize_window()
        time.sleep(10)
        div_list = web.find_elements(By.XPATH, '//*[@id="esfMain"]/section/section[3]/section[1]/section[2]/div')
        try:
            for i in div_list:
                title = i.find_element(By.XPATH, './a/div[2]/div[1]/div[1]/h3')
                title = title.text
                title = re.sub(",", " ", title)
                try:
                    span_list = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[1]/p[1]')
                    span1 = span_list.find_element(By.XPATH, './span[1]').text
                    span2 = span_list.find_element(By.XPATH, './span[2]').text
                    span3 = span_list.find_element(By.XPATH, './span[3]').text
                    span4 = span_list.find_element(By.XPATH, './span[4]').text
                    span5 = span_list.find_element(By.XPATH, './span[5]').text
                    span6 = span_list.find_element(By.XPATH, './span[6]').text
                    unitType = span1 + '' + span2 + '' + span3 + '' + span4 + '' + span5 + '' + span6
                except:
                    unitType = "NAN"
                try:
                    size = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[1]/p[2]')
                    size = size.text
                except:
                    size = "NAN"
                try:
                    Chaoxiang = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[1]/p[3]')
                    Chaoxiang = Chaoxiang.text
                except:
                    Chaoxiang = "NAN"
                try:
                    floor = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[1]/p[4]')
                    floor = floor.text
                except:
                    floor = "NAN"
                try:
                    nianfen = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[1]/p[5]')
                    nianfen = nianfen.text
                except:
                    nianfen = "NAN"
                try:
                    Community = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[2]/p[1]')
                    Community = Community.text
                except:
                    Community = "NAN"
                try:
                    span_list = i.find_element(By.XPATH, './a/div[2]/div[1]/section/div[2]/p[2]')
                    span1 = span_list.find_element(By.XPATH, './span[1]').text
                    span2 = span_list.find_element(By.XPATH, './span[2]').text
                    span3 = span_list.find_element(By.XPATH, './span[3]').text
                    address = span1 + '-' + span2 + '-' + span3
                    address = re.sub(",", "，", address)
                except:
                    address = "NAN"
                try:
                    span_list = i.find_element(By.XPATH, './a/div[2]/div[2]/p[1]')
                    span1 = span_list.find_element(By.XPATH, './span[1]').text
                    span2 = span_list.find_element(By.XPATH, './span[2]').text
                    price = span1 + '' + span2
                except:
                    price = "NAN"
                unitPrice = i.find_element(By.XPATH, './a/div[2]/div[2]/p[2]')
                unitPrice = unitPrice.text
                detail_url = i.find_element(By.XPATH, './a')
                detail_url = detail_url.get_attribute("href")
                print(
                    f"{title},{unitType},{size},{Chaoxiang},{floor},{nianfen},{Community},{address},{price},{unitPrice},{detail_url}\n")
                # 写入 csv文件
                f.write(f"{title},{unitType},{size},{Chaoxiang},{floor},{nianfen},{Community},{address},{price},{unitPrice},{detail_url}\n")
                # mongoDB数据库 - 数据持久化
                Insert_Into_MongoDB(title, unitType, size, Chaoxiang, floor, nianfen, Community, address, price,
                                    unitPrice)
                # mysql数据库 - 数据持久化
                Insert_Into_Mysql(title, unitType, size, Chaoxiang, floor, nianfen, Community, address, price,
                                  unitPrice)
        except Exception as e:
            log.write(f"{url}\n")
            print(e)
    except Exception as e:
        log.write(f"{url}\n")
        print(e)
    time.sleep(10)


if __name__ == '__main__':
    f = open("data/zz_house_info.csv", mode="a", encoding="utf-8")
    f.write(f"title,unitType,size, Chaoxiang,floor,nianfen,Community,address,unitPrice,price,detail_url\n")
    log = open("./data/log1.csv", mode="a", encoding="utf-8")
    log.write("url\n")
    for i in range(1, 3):
        url = f"https://zhengzhou.anjuke.com/sale/p{i}"
        getInfo(url, f, log)
        print("爬取" + url + " 完成！")
    f.close()
    log.close()
