import requests,re
from bs4 import BeautifulSoup
import os
import urllib.request
import lxml
url = 'http://www.mzitu.com/13022'
headers = {'Referer':'https://www.mzitu.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'}
response = requests.get(url,headers=headers)
content = response.content.decode('utf-8')
cop = BeautifulSoup(content,'lxml')

mkpath = "images\\"

menuNav = cop.find(id="menu-nav")
firstMenu = []

def urllib_download(mkdir,url,i):
  try:
    print(url)
    r = requests.get(url,headers=headers)
    with open(mkdir+'\\'+str(i)+".jpg","wb") as code:
      code.write(r.content)
  except IOError:
    print('erro')     
def imgsrc(mkdir,url,maxNum):
  try:
    downResponse = requests.get(url,headers=headers)
    downContent = downResponse.content.decode('utf-8')
    downCop = BeautifulSoup(downContent,'lxml')
    image = downCop.find(name="div",attrs='main-image')
    if (image != None):
      imagesrc = image.img.get('src')
      if (imagesrc !=None):
        urllib_download(mkdir,imagesrc,maxNum)
  except IOError:
    print('erro')      
def mkdirFile(path):
  print(path)
  try:
    path = path.strip()
    path = path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
      print(path)
      os.makedirs(path)
  except IOError:
    print('erro') 
def downlownImg(mkdir,url,len):
  for i in range(1,len):
    if(i==1):
      imgsrc(mkdir,url,i)
    else:
      imgsrc(mkdir,url+'/'+str(i),i)
def downlownLen(mkdir,url):
  try:
    downMenu = []
    downResponse = requests.get(url,headers=headers)
    downContent = downResponse.content.decode('utf-8')
    downCop = BeautifulSoup(downContent,'lxml')
    if(downCop != None):
      page =downCop.find(name="div",attrs="pagenavi")
      if(page !=None):
        for pagesize in page.find_all('a'):
          if(pagesize!=None):
            alt = pagesize.get_text()
            downMenu.append(alt)
        maxNum =int(downMenu[-2]) 
        if(maxNum!=None):
          downlownImg(mkdir,url,maxNum)
  except IOError:
    print('erro')         
def returnThreeImg(url):
  try:
    threeResponse = requests.get(url,headers=headers)
    threeContent = threeResponse.content.decode('utf-8')
    threeCop = BeautifulSoup(threeContent,'lxml')
    if(threeCop!=None):
      threeAll =threeCop.find(id="pins")
      if(threeAll!=None):
        threeAlla = threeAll.find_all('span')
        for link in threeAlla:
          if(link!=None):
            if(link.a != None):
              href = link.a.get('href')
              alt = link.a.get_text()
              mkdirFile(mkpath + alt)
              downlownLen(mkpath + alt,href)
  except IOError:
    print('erro')          
def returnSecondImg(url,num):
  try:
    for i in range(1,num+1):
      if(i==1):
        print('1----------------------------')
        print(url)
        returnThreeImg(url)
      else:
        print('url----------------------------')
        print(url + str(i))
        returnThreeImg(url + str(i))
  except IOError:  
    print('error')
def returnFirstImg(url,cop):
  try:
    page = cop.nav
    secondMenu = []
    if page !=None:
      for pagesize in page.find_all('a'):
        secondMenu.append(pagesize.get_text())
      maxNum =int(secondMenu[-2])
      
      print(maxNum)
      returnSecondImg(url,maxNum)
  except IOError:  
    print('error')    
for link in menuNav.find_all('a'):
  aSrc = link.get('href')
  firstMenu.append(aSrc)
  aResponse = requests.get(aSrc,headers=headers)
  aContent = aResponse.content.decode('utf-8')
  aCop = BeautifulSoup(aContent,'lxml')
  returnFirstImg(aSrc,aCop)
