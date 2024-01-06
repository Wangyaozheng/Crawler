import pandas as pd
from pymongo import MongoClient

# 读取CSV文件
df = pd.read_csv('E:\\大三下\\爬虫\\qimo\\sql_demo\\ajk1\\data\\zz_house_detail.csv', encoding='utf-8')
print(df.to_dict('records'))
# 连接MongoDB
client = MongoClient('localhost', 27017)
db = client['ajk_house']
collection = db['house_2']

# 将数据写入MongoDB
collection.insert_many(df.to_dict('records'))