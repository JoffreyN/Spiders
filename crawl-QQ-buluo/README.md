# 爬取QQ部落数据
## 说明
1、写的第一个爬虫，爬取QQ部落https://buluo.qq.com/p/category.html?cateid=1 中10个分类下每类100个部落的粉丝量、话题量、bid、URL等数据<br>
2、使用python3 requests库爬取数据，json库解析数据，最后用xlwt将数据写入excel，并有进度条显示<br>
3、使用的库：requests,sys,os,json,xlwt,datetime

## 注意事项
需要手动输入cookie

## 更新记录
### V1.0
- 创建文件时增加时间戳
- 优化输出，取消打印正在爬取的数据，改为进度条

### V0.7
- 优化打印，使打印输出在一行，覆盖之前的打印

### V0.6
- 优化执行速度，将请求量从上万次减少到10次；
- 动态路径
- 打印正在爬取的数据
