import requests
import json
import csv
import re
import math
import codecs


def makeData(SY,EY,i):
    data = {
        'pageSize':10,
        'dataType':1,
        'dateFrom':SY,
        'dateTo':EY,
        'sender':'盛宣怀',
        'pageth':i
    }
    return data

def main():

    with open('letterwithyearver1.csv','a',newline='') as cf:
        writer = csv.writer(cf)
        writer.writerow(['dcontributor','dsubjecs','dtitle','Year'])
        
        headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive',
            'Content-Length':'149',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'sd.library.sh.cn',
            'Origin':'http://sd.library.sh.cn',
            'Referer':'http://sd.library.sh.cn/sd/service/search/adv',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }

        for year in range(1870,1920,5):
            
            startYear = year
            endYear = year + 4
            years = str(startYear) + "-" + str(endYear)
            print(years)
            data = makeData(startYear, endYear, 1)

            r = requests.post('http://sd.library.sh.cn/sd/service/search/adv', data=data, headers=headers)
            
            getpage = re.findall('"rowCount":(.*?)}',r.text)
            #print(getpage)
            totalpage = math.floor(int(getpage[0]) / 10) + 1
            print(totalpage)
            for page in range(1,totalpage+1):
                #print(page)
                #input()
                data = makeData(startYear, endYear, page)

                r = requests.post('http://sd.library.sh.cn/sd/service/search/adv', data=data, headers=headers)

                rexlist = []
                rex = re.findall('dcontributor":"(.*?)"', r.text)
                rexlist.append(rex)
                rex = re.findall('dsubjecs":"(.*?)"', r.text)
                rexlist.append(rex)
                rex = re.findall('dtitle":"(.*?)"', r.text)
                rexlist.append(rex)

                for i in range(len(rexlist[0])):
                    arow = [rexlist[0][i].encode('utf-8'),rexlist[1][i].encode('utf-8'), rexlist[2][i].encode('utf-8'), years.encode('utf-8')]
                    print(arow)
                    writer.writerow(arow)
            
if __name__ == "__main__":
    main()

