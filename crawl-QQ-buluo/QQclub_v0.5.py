import requests
import json
import xlwt

userheaders={'Host':'buluo.qq.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0','Accept':'application/json','Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding':'gzip, deflate, br','X-Requested-With':'XMLHttpRequest','Referer':'https://buluo.qq.com/p/category.html?cateid=1','Cookie':'0','Connection':'keep-alive'}
cookie=input('输入cookies：')
userheaders['Cookie']=cookie

def getHTML(url,uheaders):
    try:
        r=requests.get(url,headers=uheaders)  
        return r.text
    except:
        return 'Connect Error'

def getResult(html):
    js=json.loads(html)
    jsresult=js['result']
    return jsresult

def getBarData(billboardid,rank):
    dataurl='https://buluo.qq.com/cgi-bin/bar/rank/category?num=100&start=0&billboard_id=%s&type=2&is_pc=1' %billboardid
    html=getHTML(dataurl,userheaders)
    jsresult=getResult(html)
    bardata=[jsresult['ranks'][rank]['rank_value'],jsresult['ranks'][rank]['gbar_name'],jsresult['ranks'][rank]['fans'],jsresult['ranks'][rank]['pids'],jsresult['ranks'][rank]['bid'],jsresult['ranks'][rank]['icon_url']]
    return bardata

def saveExcel(jsresult):
    row=['排名','部落','粉丝量','话题量','bid','URL']
    excel=xlwt.Workbook()
    for i in range(10):
        locals()['sheet%s' %i]=excel.add_sheet(jsresult['ranks'][i]['billboard_name'])
        for j in range(6):
            locals()['sheet%s' %i].write(0,j,row[j])
            for k in range(100):
                locals()['sheet%s' %i].write(k+1,j,getBarData(i+1,k)[j])
    excel.save('F:\\QQ部落.xls')

def main():
    start_url='https://buluo.qq.com/cgi-bin/bar/rank/all'    
    #print(userheaders)
    html=getHTML(start_url,userheaders)
    jsresult=getResult(html)
    saveExcel(jsresult)

main()

