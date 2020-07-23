import requests
import re
import demjson
import json
import pandas as pd
import time
import tiandetail as td

isFillColumn = False


# 尝试爬取数据
def craw():
    pageNum = 1
    url = 'http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=0&sd=2016-07-23&ed=2020-07-23&pr=120.00,500.00&sc=diy&st=desc&pi=1&pn=20&zf=diy&sh=list&rnd=0.3138604478066571'

    # csv表头
    csvColumn = []
    # csv数据集合
    csvData = []
    while (True):
        regex = re.compile("pi=\d")
        url = regex.sub('pi=' + str(pageNum), url)
        # url = url.replace('pi\d', 'pi' + str(pageNum))
        response = requests.get(url)
        if response.encoding.upper() != "UTF-8":
            response.encoding = "UTF-8"
        html = response.text

        print(html)

        # 获取列表数据
        pattern = re.compile("(\{.*?\})")
        listDataStr = re.findall(pattern, html)
        jsonData = json.loads(listDataStr[0])
        datas = [jsonData['datas']][0]
        # 跳出爬虫
        if len(datas) == 0:
            break
        # 解析数据并填充其他部分
        parseAndFill(datas, csvColumn, csvData)
        pageNum += 1

    # 保存到csv
    csv = pd.DataFrame(columns=csvColumn, data=csvData)
    timestamp = time.time()
    csv.to_csv('D:/garbage/csv/' + str(timestamp) + '.csv')


def parseAndFill(datas, csvColumn, csvData):
    splitData = []
    for data in datas:
        tmp = data.split(',')
        splitData.append(tmp)
    global isFillColumn
    if isFillColumn == False:
        csvColumn = ['代码', '基金名称', '基金类型', '净值', '日增长率', '近1周', '近1月', '近3月', '近6月', '今年来', '近1年', '近2年', '近3年', '手续费',
                     '购买起点']
        isFillColumn = True

    for row in splitData:
        id = row[0]
        rowData = []
        rowData.append(row[0])
        rowData.append(row[1])
        rowData.append(row[3])
        rowData.append(row[16])
        rowData.append(row[17])
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
        try:
            td.detail(csvColumn, rowData, id)
        except:
            print('处理的id=' + id + '的基金出错')

# 开始爬虫
craw()
