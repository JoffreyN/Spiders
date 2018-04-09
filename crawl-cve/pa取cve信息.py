import requests,openpyxl,sys,os,execjs,re,multiprocessing
from bs4 import BeautifulSoup

class Py4Js():     
	def __init__(self):  
		self.ctx=execjs.compile(""" 
        function TL(a) {
            var k="";
            var b=406644;
            var b1=3293161072;
            
            var jd=".";
            var $b="+-a^+6";
            var Zb="+-3^+b+-f";
            for (var e=[], f=0, g=0; g < a.length; g++) {
                var m=a.charCodeAt(g);
                128 > m ? e[f++]=m : (2048 > m ? e[f++]=m >> 6 | 192 : (55296==(m & 64512) && g + 1 < a.length && 56320==(a.charCodeAt(g + 1) & 64512) ? (m=65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                e[f++]=m >> 18 | 240,
                e[f++]=m >> 12 & 63 | 128) : e[f++]=m >> 12 | 224,
                e[f++]=m >> 6 & 63 | 128),
                e[f++]=m & 63 | 128)
            }
            a=b;
            for (f=0; f < e.length; f++) a +=e[f],
            a=RL(a, $b);
            a=RL(a, Zb);
            a ^=b1 || 0;
            0 > a && (a=(a & 2147483647) + 2147483648);
            a %=1E6;
            return a.toString() + jd + (a ^ b)
        };
        function RL(a, b) {
            var t="a";
            var Yb="+";
            for (var c=0; c < b.length - 2; c +=3) {
                var d=b.charAt(c + 2),
                d=d >=t ? d.charCodeAt(0) - 87 : Number(d),
                d=b.charAt(c + 1)==Yb ? a >>> d: a << d;
                a=b.charAt(c)==Yb ? a + d & 4294967295 : a ^ d
            }
            return a
        }
    """)  
          
	def getTk(self,text):  
		return self.ctx.call("TL",text)  

def translate(content):
	header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
	js=Py4Js()
	tk=js.getTk(content)
	if len(content)>4891:
		print("翻译的长度超过限制！！！")
		return
	param={'tk': tk, 'q': content}  
	r=requests.get("http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2", params=param,headers=header)  
	result=''
	for i in range(len(r.json()[0])):
		if r.json()[0][i][0]:
			result+=r.json()[0][i][0]
	return result

def GetURL(url,header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}):
	try:
		r=requests.get(url,headers=header)
		r.encoding=r.apparent_encoding
		soup=BeautifulSoup(r.text,'html.parser')
		return soup
	except Exception as e:
		print('GetURLError:%s;Reason:%s'%(url,e))

def Getdata1(cve):
	#cve英文官网
	en_description='0'
	url='http://cve.mitre.org/cgi-bin/cvename.cgi?name=%s'%cve
	try:
		soup=GetURL(url)
		en_description=soup.find(text='Description').parent.parent.next_sibling.next_sibling.contents[1].string.replace('\n',' ')
	except Exception as e:
		print('EN_cve_ERROR:%s;Reason:%s'%(cve,e))
	finally:return en_description.strip(' ')

def Getdata2(cve):
	#cve中文官网
	url='http://cve.scap.org.cn/%s.html'%cve
	vul_name,vul_level,ch_description='0','0','0'
	def VulName(s):
		l=s.split(' ',1)
		return '%s(%s)'%(l[1],l[0])

	def VulLevel(s):
		if 'HIGH' in s:level='H'
		elif 'MEDIUM' in s:level='M'
		elif 'LOW' in s:level='L'
		else:level=s
		return level

	try:
		soup=GetURL(url)
		vul_name=VulName(soup.find('meta',{'name':'description'})['content'])
		vul_level=VulLevel(soup.find('td',{'width':'67%'}).string)
		#ch_description=list(soup.find_all('td',{'colspan':'2'})[3].strings)[1].strip('\xa0')
		if list(soup.find_all('span',{'class':'tip_text'})[1].parent.next_sibling.strings)[1].strip('\xa0'):
			ch_description=list(soup.find_all('span',{'class':'tip_text'})[1].parent.next_sibling.strings)[1].strip('\xa0')
		else:ch_description=''
	except Exception as e:
		print('CH_cve_ERROR:%s;Reason:%s'%(cve,e))
	finally:return [vul_name,vul_level,ch_description]

def Getdata3(cve):
	#绿盟
	lv_vul_name,lv_affect,lv_description,lv_solution='0','0','0','0'
	url='http://www.nsfocus.net/index.php?os=&type_id=&keyword=%s&act=sec_bug&submit=+'%cve
	try:
		soup=GetURL(url)
		#lv_vul_name=soup.find('ul',{'class':'vul_list'}).a.string.replace('\xa0',' ')
		for i in soup.find('ul',{'class':'vul_list'}).children:
			get_cve=''
			try:
				href=i.a['href']
				cve_url='http://www.nsfocus.net%s'%href
				cve_soup=GetURL(cve_url)
				for strs in list(list(cve_soup.find('div',{'align':'center'}).next_siblings)[-1].strings):
					if re.match(r'^cve-\d{4}-\d{4}',strs.lower()):
						get_cve=strs
				if not get_cve:
					for strss in list(cve_soup.find(text='描述：').parent.next_siblings):
						if strss.string:
							if re.match(r'^cve-\d{4}-\d{4}',strss.string.lower()):
								get_cve=strss.string
				if get_cve.lower()==cve.lower():
					lv_vul_name=cve_soup.find('div',{'align':'center'}).b.string
					#print(href)
					if not lv_vul_name.endswith(')'):lv_vul_name=lv_vul_name+'(%s)'%cve
					lv_affect=';'.join(map(lambda s:s.strip('\n'),list(cve_soup.find('blockquote').strings)))
					data=list(list(cve_soup.find('div',{'align':'center'}).next_siblings)[-1].strings)
					startdiscrip=data.index('\n',2)+1
					datalist=list(map(lambda s:s.strip('\n'),data[startdiscrip:]))
					lv_description=''
					for k in datalist:
						if k.startswith('<*来源'):break
						if k:lv_description+=k.strip('\r\n')
					startnum,endnum=datalist.index('建议：')+1,datalist.index('浏览次数：')
					lv_solution=''.join(datalist[startnum:endnum])
					#print('绿盟名称：'+lv_vul_name+'\n绿盟影响版本：'+lv_affect+'\n绿盟描述：'+lv_description+'\n绿盟解决方案：'+lv_solution)
				else:continue
			except:continue
	except Exception as e:
		print('lv_Error:%s;Reason:%s'%(cve,e))
	finally:return [lv_vul_name,lv_affect,lv_description,lv_solution]
#Getdata3('CVE-2012-4558')

def Getcnvd(cnvd):
	def GetCookie(url='http://www.cnvd.org.cn/'):
		from selenium import webdriver
		options = webdriver.FirefoxOptions()
		options.set_headless()
		options.add_argument('-headless')
		browser=webdriver.Firefox(firefox_options=options)
		browser.get(url)
		cook=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
		browser.quit()
		return cook

	def getlevel(color):
		if 'red' in color:
			return 'H'
		elif 'yellow' in color:
			return 'M'
		elif 'green' in color:
			return 'L'
		else:return '获取失败，请手动查询。'

	def getdescrip(lists):
		try:
			descrip=lists[2].strip(' \r\n\t')
		except:
			descrip='\n'.join(map(lambda s:s.strip(' \r\n\t'),lists)).strip('\n')
		finally:
			return descrip
	header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
	header['cookie']=GetCookie()
	cnvd_cve,cnvd_name,cnvd_leve,cnvd_affect,cnvd_description,cnvd_solution='0','0','0','0','0','0'
	url='http://www.cnvd.org.cn/flaw/show/%s'%cnvd
	try:
		soup_cnvd=GetURL(url,header=header)
		cnvd_cve=soup_cnvd.find(text='CVE ID').parent.next_sibling.next_sibling.a.string.strip(' \n')
		cnvd_name=soup_cnvd.find('div',{'class':'blkContainerSblk'}).h1.string.strip(' \n')
		if not cnvd_name.endswith(')'):cnvd_name=cnvd_name+'(%s)'%cnvd_cve
		cnvd_leve=getlevel(soup_cnvd.find('td',{'class':'denle'}).span['class'][0])
		cnvd_affect='\n'.join(map(lambda s:s.strip(' \r\n\t'),list(list(soup_cnvd.find(text='影响产品').parent.next_siblings)[1].strings))).strip('\n')
		cnvd_description=getdescrip(list(soup_cnvd.find(text='漏洞描述').parent.next_sibling.next_sibling.strings))
		cnvd_solution='\n'.join(map(lambda s:s.strip(' \r\n\t'),list(soup_cnvd.find(text='漏洞解决方案').parent.next_sibling.next_sibling.strings))).strip('\n')
	except Exception as e:
		print('cnvd_ERROR:%s;Reason:%s'%(cnvd,e))
	finally:return [cnvd_cve,cnvd,cnvd_name,cnvd_leve,cnvd_affect,cnvd_description,cnvd_solution]
#cnvd_list=Getcnvd('CNVD-2013-01681')
#print(cnvd_list)

def Getcnnvd(cnnvd):
	cnnvd_cve,cnnvd_name,cnnvd_leve,cnnvd_description,cnnvd_solution='0','0','0','0','0'
	def getstring(siblings):
		string=''
		for i in siblings:
			if i.string:
				string+=i.string.strip(' \r\n\t')+'\n'
			else:continue
		#print(string.strip('\n'))
		return string.strip('\n')

	def getleve(s):
		if '高' in s:return 'H'
		elif '中' in s:return 'M'
		elif '低' in s:return 'L'
		else:return '获取失败，请手动查询。'

	url='http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=%s'%cnnvd
	try:
		soup_cnnvd=GetURL(url)
		cnnvd_name=soup_cnnvd.find('div',{'class':'detail_xq w770'}).h2.string
		cnnvd_cve=soup_cnnvd.find(text='CVE编号：').parent.parent.a.string.strip(' \r\n\t')
		if not cnnvd_name.endswith(')'):cnnvd_name=cnnvd_name+'(%s)'%cnnvd_cve
		cnnvd_leve=getleve(list(soup_cnnvd.find(text='危害等级：').parent.parent.a.strings)[0].strip(' \r\n\t'))
		cnnvd_description=soup_cnnvd.find('div',{'class':'d_ldjj'}).p.next_sibling.string.strip(' \r\n\t')
		cnnvd_solution=getstring(soup_cnnvd.find('div',{'class':'d_ldjj m_t_20'}).children)
	except Exception as e:
		print('cnnvd_ERROR:%s;Reason:%s'%(cnnvd,e))
	finally:return [cnnvd_cve,cnnvd,cnnvd_name,cnnvd_leve,cnnvd_description,cnnvd_solution]

if __name__=='__main__':
	if os.path.isfile(sys.argv[1]):
		savepath=os.path.splitext(sys.argv[1])[0]+'.xlsx'
		excel=openpyxl.Workbook()
		cve_sheet,cve_sheet.title,cnvd_sheet,cnnvd_sheet=excel.active,'cve_CH_EN_LV',excel.create_sheet('cnvd'),excel.create_sheet('cnnvd')
		cve_sheet.append(['cve','vul_name','vul_level','ch_description','en_description','GoogleTranslate','lv_vul_name','lv_affect','lv_description','lv_solution'])
		cnvd_sheet.append(['cve编号','cnvd编号','cnvd名称','cnvd等级','cnvd描述','cnvd解决方案'])
		cnnvd_sheet.append(['cve编号','cnnvd编号','cnnvd名称','cnnvd等级','cnnvd描述','cnnvd解决方案'])
		for i in open(sys.argv[1],'r',encoding='utf8'):
			code=i.strip('\n')
			sys.stdout.write('正在处理：%s'%code+'      \r')
			sys.stdout.flush()
			try:
				if code.lower().startswith('cve'):
					en_description=Getdata1(code)
					cve_lists=sum([[code],Getdata2(code),[en_description,translate(en_description)],Getdata3(code)],[])
					cve_sheet.append(cve_lists)
				elif code.lower().startswith('cnvd'):
					cnvd_list=Getcnvd(code)
					cnvd_sheet.append(cnvd_list)
				elif code.lower().startswith('cnnvd'):
					cnnvd_list=Getcnnvd(code)
					cnnvd_sheet.append(cnnvd_list)
				else:
					print('Error:%s'%code)
					continue
			except:continue
		excel.save(savepath)
		print('\n完成！保存路径：%s'%savepath)
	else:
		try:
			for i in Getdata2(sys.argv[1]):
				print(i)
			print(Getdata1(sys.argv[1]))
			lv=Getdata3(cve)
			print('绿盟名称：'+lv[0]+'\n绿盟影响版本：'+lv[1]+'\n绿盟描述：'+lv[2]+'\n绿盟解决方案：'+lv[3])
		except Exception as e:
			print('InputError:%s'%e)
#pa取cve信息.py CVE-2013-2067
#pa取cve信息.py E:\ZP\Desktop\cve.txt
