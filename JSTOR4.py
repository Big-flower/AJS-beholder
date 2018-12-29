##--------------------------------JSTOR-------------------------------------------------
##----------------------------ASR(1936-2015)-------------------------------------

##----------------------------import section-----------------------------

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import http.cookiejar
import urllib.request
from urllib.parse import urljoin
import re
import csv
import time
import random
import pygame
##----------------------------def section-----------------------------------------
##用來從更目錄中得到的issue的url
def uleissue(bs):
    urlpool=[]
    for link in bs.find_all('a'):
        if 'href' in link.attrs:
            a=link.attrs['href']
            tf='stable' in a
            if tf==True: 
                b=urljoin('https://www.jstor.org',a)
                urlpool.append(b)
    return urlpool

##export into csv
def eptcsv(filelist,address):
    with open(address , 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        writer.writerows(filelist)
    return()

## import from csv
def ipfcsv(address):
    with open(address, newline='') as csvfile:
        rows = csv.reader(csvfile)
        finalpool=[]
        for row in rows:
            row[0]=row[0].replace(' ','')
            finalpool=row+finalpool
    return(finalpool) 

##save article detail in csv
def article_detail_into_csv(address,listname):
    with open(address, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(listname)
    return()

##playmusic
def playmusic(path):
    pygame.mixer.init()
    track1=pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    return()

##----------------------------將clean article url pool 分成幾個部分（保存為新的，就不再重複）-----------------------------
cleanarpool=ipfcsv('/Users/FANG/local file/curriculum.G3.1/Python for Humanities/articalurlpoolclean.csv')
random.shuffle(cleanarpool)
eptcsv(cleanarpool,'/Users/FANG/local file/curriculum.G3.1/Python for Humanities/articleurlpoolcleanrandom.csv')
##上面已經產生了articleurlpoolcleanrandom.csv中保存了隨機順序的url pool
##導入數據
cleanarpool=ipfcsv('/Users/FANG/local file/curriculum.G3.1/Python for Humanities/articleurlpoolcleanrandom.csv')
atpdict={}
j=1
for i in range(0,len(cleanarpool),50):
    name='subatpool'+str(j)
    atpdict[name]=cleanarpool[i:i+50]
    j=j+1


##----------------------------單頁面測試-----------------------------
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}

urlr=atpdict['subatpool1'][0]#review
responser = requests.get(urlr, headers=headers)
htmlr=responser.text
bsr = BeautifulSoup(htmlr, 'html.parser')##得到bsr

urla=atpdict['subatpool1'][3]#article
responsea = requests.get(urla, headers=headers)
htmla=responsea.text
bsa = BeautifulSoup(htmla, 'html.parser')##得到bsa


'''
itemr=bsr.find_all('h1',{'data-qa':'item-title'})
itemrec=itemr[0].text.replace('\n','').strip()

itema=bsa.find_all('h1',{'data-qa':'item-title'})
itemaec=itema[0].text.replace('\n','').strip()
'''


##----------------------------頁面一般性代碼(50頁測試，subatpool1)-----------------------------

#artical_detail_list=[]
artical_detail_each=[]

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}
for i in range(0,len(atpdict['subatpool1'])):
    url=atpdict['subatpool1'][i]
    response = requests.get(url, headers=headers)
    if response.status_code==200:
        html=response.text
        bs = BeautifulSoup(html, 'html.parser')
        titletr=bs.find('h1').text.replace('\n','').strip()
        if titletr=='Review':
            print(i,'review')
        else:
            #title
            artical_detail_each.append(titletr)
            #author          
            item_author=bs.find_all('div' , class_='contrib')
            if item_author!=[]:
                item_author_f=item_author[0].text.replace('\n','').strip() 
                artical_detail_each.append(item_author_f)
            else:
                print(titletr)
                print(url)
                artical_detail_each.append('.')
            #number
            item_number=bs.find_all('div' , class_='src')
            if item_number!=[]:
                item_number_f=item_number[0].text.replace('\n','').strip()
                artical_detail_each.append(item_number_f)
            else: 
                artical_detail_each.append('.')
            #abstract
            item_abstract=bs.find_all('div' , class_='abstract1')
            if item_abstract!=[]:
                item_abstract_f=item_abstract[0].text.replace('\n','').strip()
                artical_detail_each.append(item_abstract_f)
            else:
                artical_detail_each.append('.')
            artical_detail_each.append(url)
            print(i)
            artical_detail_list.append(artical_detail_each)
            artical_detail_each=[]
    else:
        print('wrong')
        print(i)
    sleeptime=random.randint(7,21)
    time.sleep(sleeptime)

##----------------------------一般性代碼()-----------------------------
#artical_detail_list=[]
 artical_detail_each=[]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}

lst=[]
for j in atpdict.keys():
    lst.append(j)

for k in lst:
    print(k)
    for i in range(0,len(atpdict[k])):
        url=atpdict[k][i]
        response = requests.get(url, headers=headers)
        if response.status_code==200:
            html=response.text
            bs = BeautifulSoup(html, 'html.parser')
            titletr=bs.find('h1').text.replace('\n','').strip()
            if titletr=='Review':
                print(i,'review')
            else:
                #title
                artical_detail_each.append(titletr)
                #author          
                item_author=bs.find_all('div' , class_='contrib')
                if item_author!=[]:
                    item_author_f=item_author[0].text.replace('\n','').strip() 
                    artical_detail_each.append(item_author_f)
                else:
                    print(titletr)
                    print(url)
                    artical_detail_each.append('.')
                #number
                item_number=bs.find_all('div' , class_='src')
                if item_number!=[]:
                    item_number_f=item_number[0].text.replace('\n','').strip()
                    artical_detail_each.append(item_number_f)
                else: 
                    artical_detail_each.append('.')
                #abstract
                item_abstract=bs.find_all('div' , class_='abstract1')
                if item_abstract!=[]:
                    item_abstract_f=item_abstract[0].text.replace('\n','').strip()
                    artical_detail_each.append(item_abstract_f)
                else:
                    artical_detail_each.append('.')
                artical_detail_each.append(url)
                print(i)
                artical_detail_list.append(artical_detail_each)
                artical_detail_each=[]
        else:
            print('wrong')
            print(i)
        sleeptime=random.randint(7,21)
        time.sleep(sleeptime)




'''
aaa=artical_detail_list
##replace('','.')
bbb=[]
ccc=[]
for i in aaa:
    for j in i:
        if j=='':
            b=j.replace('','.')
            ccc.append(b)
        else:
            ccc.append(j)
    bbb.append(ccc)
    ccc=[]
'''
           
##--------------------------------------中间断了，接着写完subatpool31------------------------------------------
artical_detail_each=[]

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}
for i in range(15,len(atpdict['subatpool183'])):
    url=atpdict['subatpool100'][i]
    response = requests.get(url, headers=headers)
    if response.status_code==200:
        html=response.text
        bs = BeautifulSoup(html, 'html.parser')
        titletr=bs.find('h1').text.replace('\n','').strip()
        if titletr=='Review':
            print(i,'review')
        else:
            #title
            artical_detail_each.append(titletr)
            #author          
            item_author=bs.find_all('div' , class_='contrib')
            if item_author!=[]:
                item_author_f=item_author[0].text.replace('\n','').strip() 
                artical_detail_each.append(item_author_f)
            else:
                print(titletr)
                print(url)
                artical_detail_each.append('.')
            #number
            item_number=bs.find_all('div' , class_='src')
            if item_number!=[]:
                item_number_f=item_number[0].text.replace('\n','').strip()
                artical_detail_each.append(item_number_f)
            else: 
                artical_detail_each.append('.')
            #abstract
            item_abstract=bs.find_all('div' , class_='abstract1')
            if item_abstract!=[]:
                item_abstract_f=item_abstract[0].text.replace('\n','').strip()
                artical_detail_each.append(item_abstract_f)
            else:
                artical_detail_each.append('.')
            artical_detail_each.append(url)
            print(i)
            artical_detail_list.append(artical_detail_each)
            artical_detail_each=[]
    else:
        print('wrong')
        print(i)
        break
    sleeptime=random.randint(7,22)
    time.sleep(sleeptime)
playmusic('/Users/FANG/local file/PythonForHumanities/musical-cue.mp3')


'''
for k in lst:
    for i in range(0,len(atpdict[k])):
        url=atpdict[k][i]
        if url==aaa:
            print(k)
            print(i)

'''

##--------------------------------------从subatpool32开始------------------------------------------
lst1=lst
lst1=lst1[100:]

artical_detail_each=[]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}

for k in lst1:
    print(k)
    for i in range(0,len(atpdict[k])):
        url=atpdict[k][i]
        response = requests.get(url, headers=headers)
        if response.status_code==200:
            html=response.text
            bs = BeautifulSoup(html, 'html.parser')
            titletr=bs.find('h1').text.replace('\n','').strip()
            if titletr=='Review':
                print(i,'review')
            else:
                #title
                artical_detail_each.append(titletr)
                #author          
                item_author=bs.find_all('div' , class_='contrib')
                if item_author!=[]:
                    item_author_f=item_author[0].text.replace('\n','').strip() 
                    artical_detail_each.append(item_author_f)
                else:
                    print(titletr)
                    print(url)
                    artical_detail_each.append('.')
                #number
                item_number=bs.find_all('div' , class_='src')
                if item_number!=[]:
                    item_number_f=item_number[0].text.replace('\n','').strip()
                    artical_detail_each.append(item_number_f)
                else: 
                    artical_detail_each.append('.')
                #abstract
                item_abstract=bs.find_all('div' , class_='abstract1')
                if item_abstract!=[]:
                    item_abstract_f=item_abstract[0].text.replace('\n','').strip()
                    artical_detail_each.append(item_abstract_f)
                else:
                    artical_detail_each.append('.')
                artical_detail_each.append(url)
                print(i)
                artical_detail_list.append(artical_detail_each)
                artical_detail_each=[]
        else:
            print('wrong')
            print(i)
            break
        sleeptime=random.randint(8,22)
        time.sleep(sleeptime)


##--------------------------------------加點功能------------------------------------------
lst1=lst
lst1=lst1[183:]
absentlist=[]
artical_detail_each=[]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}

for k in lst1:
    print(k)
    for i in range(0,len(atpdict[k])):
        url=atpdict[k][i]
        response = requests.get(url, headers=headers)
        if response.status_code==200:
            html=response.text
            bs = BeautifulSoup(html, 'html.parser')
            titletr=bs.find('h1').text.replace('\n','').strip()
            if titletr=='Review':
                print(i,'review')
            else:
                #title
                artical_detail_each.append(titletr)
                #author          
                item_author=bs.find_all('div' , class_='contrib')
                if item_author!=[]:
                    item_author_f=item_author[0].text.replace('\n','').strip() 
                    artical_detail_each.append(item_author_f)
                else:
                    print(titletr)
                    print(url)
                    artical_detail_each.append('.')
                #number
                item_number=bs.find_all('div' , class_='src')
                if item_number!=[]:
                    item_number_f=item_number[0].text.replace('\n','').strip()
                    artical_detail_each.append(item_number_f)
                else: 
                    artical_detail_each.append('.')
                #abstract
                item_abstract=bs.find_all('div' , class_='abstract1')
                if item_abstract!=[]:
                    item_abstract_f=item_abstract[0].text.replace('\n','').strip()
                    artical_detail_each.append(item_abstract_f)
                else:
                    artical_detail_each.append('.')
                artical_detail_each.append(url)
                print(i)
                artical_detail_list.append(artical_detail_each)
                artical_detail_each=[]
        else:
            print('wrong')
            print(k)
            print(i)
            absentlist.append(url)
            playmusic('/Users/FANG/local file/PythonForHumanities/musical-cue.mp3')
            time.sleep(600)
        sleeptime=random.randint(8,22)
        time.sleep(sleeptime)




article_detail_into_csv('/Users/FANG/local file/curriculum.G3.1/Python for Humanities/articledetail4.csv',artical_detail_list)
eptcsv(absentlist,'/Users/FANG/local file/curriculum.G3.1/Python for Humanities/absenturl3.csv')

