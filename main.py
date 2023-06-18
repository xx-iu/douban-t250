# -*- coding = utf-8 -*-
# @Time : 2022/1/27 20:41
# @Author : xuxiang
# @File : main.py

import os
from bs4 import BeautifulSoup #网页解析 获取数据
import urllib.request, urllib.error
import re    #正则表达式 文字匹配
import sqlite3 #存数据库
import xlwt
import sys

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #爬取网页
    datalist = getData(baseurl)
    savepath = "douban250.xls"
    #解析数据
    #保存数据
    saveData(datalist, savepath)
    #askURL("https://movie.douban.com/top250?start=0")
    #爬取网页

#影片详情
findlink = re.compile(r'<a href="(.*?)">')
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findjudge = re.compile(r'<span>(\d*)人评价</span>')
#概括
findinq = re.compile(r'<span class="inq">(.*)</span>')
#影片相关内容
findbd = re.compile(r'<p class="">(.*?)</p>', re.S)

def getData(baseurl):
    datalist =[]
    for i in range(0, 10):
        url = baseurl + str(i*25)
        html = askURL(url)   # 保存
    # 逐一分析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_='item'):
            # print(item)
            data = []
            item = str(item)
            link = re.findall(findlink, item)[0]     #正则匹配影片链接
            data.append(link)       #添加链接

            image = re.findall(findImgSrc, item)[0]
            data.append(image)      #添加图片

            titles = re.findall(findTitle, item)
            if(len(titles) == 2):
                ctitle = titles[0]     #添加标题
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)  #添加外文名
            else:
                data.append(titles[0])
                data.append(' ')

            rating = re.findall(findRating, item)[0]
            data.append(rating)  #添加评分

            judgenum = re.findall(findjudge, item)[0]
            data.append(judgenum)   #添加评分人数

            inq = re.findall(findinq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)        #添加概括
            else:
                data.append(" ")

            bd = re.findall(findbd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())

            datalist.append(data)   #处理好的一部放入datalist

    return datalist

# 指定一个url的网页内容
def askURL(url):
    head ={
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 97.0.4692.99 Safari / 537.36 Edg / 97.0.1072.69"
    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response =urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#保存数据
def saveData(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("豆瓣电影top250",cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片英外文名", "评分", "评分人数", "概括", "相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])    #数据

    book.save('douban250.xls')

if __name__=="__main__":
    main()
    print("爬取完毕!")