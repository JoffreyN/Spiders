# 爬取cve信息
使用python3编写，从http://cve.mitre.org 、http://cve.scap.org.cn 、http://www.nsfocus.net 、http://www.cnvd.org.cn 中爬取cve名称、描述、严重等级、影响范围、解决方案等信息。同时将爬下来的英文使用谷歌翻译成中文，最终将所有数据保存为excel。后期将考虑同时写入数据库和使用多进程提升效率

## 使用
~~~
pa取cve信息.py E:\ZP\Desktop\cve.txt
  #cve.txt样例见目录，运行结果见cve.xlsx
~~~

## 说明
1、使用requests爬取数据，使用BeautifulSoup解析网页，提取数据，动态打印正在爬取的cve号<br>
2、其中谷歌翻译和cnvd官网有反爬虫策略，谷歌翻译反爬虫策略已有大牛破解，地址https://github.com/cocoa520/Google_TK ；cnvd官网的策略是在cookie中需要两个参数__jsluid、__jsl_clearance，它们的值都是经js计算的，这里懒得分析js代码，直接使用selenium的-headless模式获取cookie，只需获取一次，后续只要判断该cookie是否有效即可
