import re

pageNum = 2
url = 'http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=0&sd=2016-07-23&ed=2020-07-23&pr=120.00,500.00&sc=diy&st=desc&pi=1&pn=20&zf=diy&sh=list&rnd=0.3138604478066571'
regex = re.compile("pi=\d")

sl = regex.findall(url)
print(sl)

url = regex.sub('pi=' + str(pageNum), url)
print(url)