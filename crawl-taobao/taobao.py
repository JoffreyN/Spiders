import requests
import re
def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def parserPage(ilt,html):
    try:
        plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt=re.findall(r'\"raw_title\"\:\".*?\"',html)
        lin=re.findall(r'\"comment_url\"\:\".*?\"',html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            link=eval(lin[i].split(':')[1])
            ilt.append([price,title,link])
    except:
        print("")

def printGoodsList(ilt):
    tplts="{:4}\t{:8}\t{:44}\t\thttps:{}"
    tplt="{:4}\t{:8}\t{:16}\t\t\t\t\t\t{}"
    print(tplt.format("序号","价格","商品名称","链接"))
    count=0
    for g in ilt:
        count=count+1
        print(tplts.format(count,g[0],g[1],g[2]))
    print()

def main():
    goods='三星s8+'
    depth=1
    start_url='https://s.taobao.com/search?q='+goods
    infoList=[]
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=getHTMLText(url)
            parserPage(infoList,html)
        except:
            continue
    printGoodsList(infoList)
main()
