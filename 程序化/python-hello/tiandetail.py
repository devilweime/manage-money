import requests

def detail(columnFlied,rowData,id) :
    url = 'http://fund.eastmoney.com/pingzhongdata/'+id+'.js?v=20200721231843'
    resp = requests.get(url)
    if resp.encoding.upper() != "UTF-8":
        resp.encoding = 'UTF-8'
    html = resp.text()