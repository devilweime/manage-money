import re
import time
import demjson
import matplotlib.pyplot as plt
import requests


html = requests.get("http://fund.eastmoney.com/pingzhongdata/000522.js?v=20160518155842").text

dataPattern = re.compile("var Data_netWorthTrend = (\[.*?\]);")
targetStr = re.findall(dataPattern, html)
equityDataList = demjson.decode(targetStr[0])
print(equityDataList)

for item in equityDataList:
    item['x'] = time.strftime("%Y-%m-%d", time.localtime(item['x'] / 1000))

xData = list(map(lambda item: item.get('x'), equityDataList))
yData = list(map(lambda item: item.get('y'), equityDataList))

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 一个基本的折线图
plt.figure(figsize=(12, 5))
plt.title("华润元大信息传媒科技混合-单位净值走势折线图")
# 收盘价的折线图
plt.xlabel("日期")

# x=[]
# for i in range(0,len(xData),30):
#     x.append(xData[i])

plt.xticks([i for i in range(0, len(xData), 30)], [xData[i] for i in range(0, len(xData), 30)], rotation=45)
plt.plot_date(xData, yData, '-', label="单位净值")

print(yData[-1], yData[-2])
difValue = yData[-1] - yData[-2]
print(difValue / yData[-2])

plt.show()
