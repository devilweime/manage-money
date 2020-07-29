import time

import requests
import demjson

isFillColumns = False


# 爬取波动率、夏普比率、回撤率
def craw(columns, rowData, id):
    global isFillColumns
    if isFillColumns == False:
        columns.append('近1年夏普比率')
        columns.append('近1年波动率')
        columns.append('近1年最大回撤')
        columns.append('近1年收益回撤比')
        columns.append('近1月定投人数')
        columns.append('近1月访问量')
        columns.append('近1月加自选总人数')
        columns.append('用户平均持有时长')
        isFillColumns =True

    url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNUniqueInfo'
    host = 'fundmobapi.eastmoney.com'
    headers = {
        'Host': host
    }

    params = {
        'version': '6.2.7',
        'plat': 'Android',
        'appType': 'ttjj',
        'FCODE': id,
        'onFundCache': '3',
        'keeeeeyparam': 'FCODE',
        'deviceid': 'fde28b4362b862450bd28f9a690a145e%7C%7Ciemi_tluafed_me',
        'igggggnoreburst': 'true',
        'product': 'EFund',
        'MobileKey': 'fde28b4362b862450bd28f9a690a145e%7C%7Ciemi_tluafed_me',
        'gToken': 'ceaf-e4ab5262edb2ddc485abde8a9e1e6580'
    }

    requests.packages.urllib3.disable_warnings()
    apiData = requests.post(url, data=params, headers=headers, verify=False, timeout=10000).text

    apiObj = demjson.decode(apiData)
    datas = apiObj['Datas']

    rowData.append(datas['SHARP1'])
    rowData.append(datas['STDDEV1'])
    rowData.append(datas['MAXRETRA1'])
    rowData.append(datas['SHARP1'])
    rowData.append(datas['DTCOUNT_Y'])
    rowData.append(datas['PV_Y'])
    rowData.append(datas['FFAVORCOUNT'])
    rowData.append(datas['AVGHOLD'])

    time.sleep(1)



# craw([], [], '161725')
