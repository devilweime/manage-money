import requests
import re
import demjson
import json
import pandas as pd
import time

response = requests.get(
    "http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=0&sd=&ed=&sc=3y&st=desc&pi=1&pn=20&zf=diy&sh=list")
if response.encoding.upper() != "UTF-8":
    response.encoding = "UTF-8"
html = response.text

print(html)

# 获取列表数据
pattern = re.compile("(\{.*?\})")
listDataStr = re.findall(pattern, html)
jsonData = json.loads(listDataStr[0])
datas = [jsonData['datas']][0]

splitData = []
for data in datas:
    tmp = data.split(',')
    splitData.append(tmp)

columnFlied = ['基金名称|代码', '基金类型', '净值|日增长率', '近1周', '近1月', '近3月', '近6月', '今年来', '近1年', '近2年', '近3年', '手续费|购买起点']
csv = pd.DataFrame(columns=columnFlied,splitData)
time = time.time()
csv.to_csv('/csv/'+time+'.csv')
print(splitData)
