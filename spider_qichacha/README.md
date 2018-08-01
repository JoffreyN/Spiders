企查查爬虫
===========================
1. 根据企业注册号在企查查中爬取企业信息，将爬取的结果存入数据库，同时保存为excel。
2. 爬取数据时会先查询数据库，如果数据库中有该数据且是3个月之内存入的，则从数据库中取该数据。

****
	
|Author|E-mail|
|---|---
|Joffrey|Joffrey@foxmail.com

### 部署运行环境
1. 安装火狐最新版
2. 安装python3.6以上版本(安装时勾选 添加到PATH)
3. 将geckodriver.exe移动至python安装目录(~Python36\)下
4. 安装python依赖库
```python
  管理员打开cmd，运行下列命令：
  pip install pandas faker bs4 selenium pymysql
```
5. 测试MySQL连接
```
  MySQL所在网络为Bestpay-FSX
  192.168.4.47 zp 123456
```
### 开始爬取
1. 将要爬取的企业注册号放入companyID.txt中，一行一个
2. 双击qichacha_spider.py，开始运行

****

### 反反爬虫
|#|反爬虫|反反爬虫|
|---|---|----
|1|cookie限制|selenium自动登陆获取cookie
|2|点选汉字验证码限制登陆|QQ登陆绕过验证码
|3|限制IP访问次数|X-Forwarded-For伪造IP来源

### 其它说明
1. 在企查查页面中股东信息表里，如果是公司名，则爬取该公司基本信息，否则跳过
2. 暂无法从企查查页面变更记录表中解析出 历史法人、历史股东（投资人、管理层）相关信息
3. 暂未使用爬虫框架以及多线程，后期有需要再进行开发
