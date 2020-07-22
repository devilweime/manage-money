import requests
import re
import demjson
from lxml import etree


def detail(columns, rowData, id):
    detail1(columns, rowData, id)
    # detail2(columns, rowData, id)


# # 获取 成立日期、规模等信息
def detail1(columns, rowData, id):
    # url = 'http://fund.eastmoney.com/' + id + '.html'
    url = 'https://www.baidu.com/'
    resp = requests.get(url)
    resp.encoding = 'UTF-8'
    html = resp.text
    print(html)
    tree = etree.HTML(html)
    parent = tree.xpath('//*[@id="s-bottom-layer-right"]/span[3]/text()')
    print(parent)
    print(parent[0])
    #parent = tree.xpath('//div[@class="infoOfFund"]//table')
    size = parent[0].xpath("./tbody/tr[1]/td[2]")
    print(size)


# # 获取 图形数据、经理信息
def detail2(columns, rowData, id):
    url = 'http://fund.eastmoney.com/pingzhongdata/' + id + '.js?v=20200722080726'
    html = requests.get(url).text
    print(html)
    pattern = re.compile('var Data_currentFundManager =(\[.*?\]) ;')
    targetData = re.findall(pattern, html)
    dataList = demjson.decode(targetData[0])
    print(dataList)

    columns.append('经理')
    columns.append('经理任期')
    columns.append('任期收益')
    columns.append('同类平均')
    columns.append('沪深300')
    columns.append('任期收益环比同类')
    columns.append('任期收益环比沪深300')

    manager = dataList[0]

    rowData.append(manager['name'])
    rowData.append(manager['workTime'])
    p1 = manager['profit']['series'][0]['data'][0]['y']
    p2 = manager['profit']['series'][0]['data'][1]['y']
    p3 = manager['profit']['series'][0]['data'][2]['y']
    rowData.append(p1)
    rowData.append(p2)
    rowData.append(p3)
    rowData.append(p1 / p2)
    rowData.append(p1 / p3)

    print(columns)
    print(rowData)


detail([], [], '002542')
