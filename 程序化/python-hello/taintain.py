import requests
import re
import demjson
import json
import pandas as pd
import time
import tiandetail as td

response = requests.get(
    # "http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=0&sd=&ed=&sc=3y&st=desc&pi=1&pn=20&zf=diy&sh=list"
    "http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=0&rs=6y,100&sd=&ed=&sc=6y&st=desc&pi=1&pn=20&zf=diy&sh=list&rnd=0.8516450784808944"
)
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

columnFlied = ['代码', '基金名称', '基金类型', '净值', '日增长率', '近1周', '近1月', '近3月', '近6月', '今年来', '近1年', '近2年', '近3年', '手续费',
               '购买起点']
csvData = []
for row in splitData:
    id = row[0]
    rowData = []
    rowData.append(row[0])
    rowData.append(row[1])
    rowData.append(row[3])
    rowData.append(row[16])
    rowData.append(row[17] + '%')
    rowData.append(row[5])
    rowData.append(row[6])
    rowData.append(row[7])
    rowData.append(row[8])
    rowData.append(row[4])
    rowData.append(row[9])
    rowData.append(row[10])
    rowData.append(row[11])
    rowData.append(row[19] + '|' + row[22])
    rowData.append(row[20])
    csvData.append(rowData)
    td.detail(columnFlied, rowData, id)

csv = pd.DataFrame(columns=columnFlied, data=csvData)
time = time.time()
csv.to_csv('G:/garbage/csv/' + str(time) + '.csv')
print(csvData)
