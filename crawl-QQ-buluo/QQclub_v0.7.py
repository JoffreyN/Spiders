import requests,sys,os,json,xlwt,time

'''
V0.7
优化打印，使打印输出在一行，覆盖之前的打印
--------------------------
V0.6
优化执行速度，将请求量从上万次减少到10次；
动态路径
打印正在爬取的数据
'''

path=os.getcwd()+'\\QQ部落.xls'
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

def getallData(billboardid):
    dataurl='https://buluo.qq.com/cgi-bin/bar/rank/category?num=100&start=0&billboard_id=%s&type=2&is_pc=1' %billboardid
    html=getHTML(dataurl,userheaders)
    jsresult=getResult(html)
    alldata=[]
    for rank in range(100):
        onedata=[jsresult['ranks'][rank]['rank_value'],jsresult['ranks'][rank]['gbar_name'],jsresult['ranks'][rank]['fans'],jsresult['ranks'][rank]['pids'],jsresult['ranks'][rank]['bid'],jsresult['ranks'][rank]['icon_url']]
        alldata.append(onedata)
    return alldata

def saveExcel(jsresult):    
    row=['rankID','部落','粉丝量','话题量','bid','URL']
    excel=xlwt.Workbook()
    for i in range(10):
        alldata=getallData(i+1)
        locals()['sheet%s' %i]=excel.add_sheet(jsresult['ranks'][i]['billboard_name'])
        for j in range(6):
            locals()['sheet%s' %i].write(0,j,row[j])
            for k in range(100):
                locals()['sheet%s' %i].write(k+1,j,alldata[k][j])
                string='正在爬取数据:'+str(alldata[k][j])                
                time.sleep(0.01)
                sys.stdout.write('正在爬取数据:'+' '*100+'\r')
                sys.stdout.flush()
                sys.stdout.write(string+'\r')
                sys.stdout.flush()
    excel.save(path)
    print('爬取完毕！'+' '*99)

def main():
    print('文件将保存至：{}\n'.format(path))
    start_url='https://buluo.qq.com/cgi-bin/bar/rank/all'    
    html=getHTML(start_url,userheaders)
    jsresult=getResult(html)
    saveExcel(jsresult)

main()

