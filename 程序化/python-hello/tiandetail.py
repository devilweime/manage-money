import requests

import re
import demjson
from lxml import etree

fillColumns1 = False
fillColumns2 = False


def detail(columns, rowData, id):
    detail1(columns, rowData, id)
    detail2(columns, rowData, id)


# # 获取 成立日期、规模等信息
def detail1(columns, rowData, id):
    # print(rowData[1])
    url = 'http://fund.eastmoney.com/' + id + '.html'
    resp = requests.get(url)
    resp.encoding = 'UTF-8'
    html = resp.text
    tree = etree.HTML(html)
    # tableData = tree.xpath('//div[@class="infoOfFund"]/table/tbody//text()')
    tds = tree.xpath('//div[@class="infoOfFund"]//td')

    tableData = []
    for td in tds:
        tmp = etree.tostring(td, encoding='utf-8', method="text").decode('utf-8')
        tableData.append(tmp)

    print(tableData)

    global fillColumns1
    if fillColumns1 == False:
        columns.append('基金规模(亿元)')
        columns.append('成 立 日')
        columns.append('管 理 人')
        # columns.append('基金评级')
        fillColumns1 = True
    tmp = tableData[1]
    index = tmp.find('亿') - 1
    size = tmp[tmp.find("：") + 1:index]
    rowData.append(size)
    tmp = tableData[3]
    rowData.append(tmp[tmp.find("：") + 1:-1])
    tmp = tableData[4]
    rowData.append(tmp[tmp.find("：") + 1:-1])
    # rowData.append(tableData[14])

    print(columns)
    print(rowData)


# # 获取 图形数据、经理信息
def detail2(columns, rowData, id):
    url = 'http://fund.eastmoney.com/pingzhongdata/' + id + '.js?v=20200722080726'
    html = requests.get(url).text
    print(html)
    pattern = re.compile('var Data_currentFundManager =(\[.*?\]) ;')
    targetData = re.findall(pattern, html)
    dataList = demjson.decode(targetData[0])

    global fillColumns2
    if fillColumns2 == False:
        columns.append('经理')
        columns.append('经理任期')
        columns.append('任期收益')
        columns.append('同类平均')
        columns.append('沪深300')
        columns.append('任期收益环比同类')
        columns.append('任期收益环比沪深300')
        fillColumns2 = True

    manager = dataList[0]

    rowData.append(manager['name'])
    rowData.append(manager['workTime'])

    bar = manager['profit']['series'][0]['data']

    p1 = bar[0]['y']
    p2 = bar[1]['y']
    p3 = 0
    if len(bar) == 3:
        p3 = bar[2]['y']

    rowData.append(p1)
    rowData.append(p2)
    rowData.append(p3)
    rowData.append(p1 / p2)
    rowData.append(0) if p3 == 0 else rowData.append(p1 / p3)

    print(columns)
    print(rowData)


## detail([], [], '001766')
