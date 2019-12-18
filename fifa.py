
import requests
import json
import pandas as pd
import re
import os
import sys
import urllib.request
import datetime
import time
import json
import csv

from bs4 import BeautifulSoup

fifa_rank = "https://www.fifa.com/fifa-world-ranking/ranking-table/men/"
fifa_rank_html = requests.get(fifa_rank)
fifa_rank_html_list =  BeautifulSoup(fifa_rank_html.content ,"html.parser" ,from_encoding='utf=8')

fifa_rank_list = fifa_rank_html_list.select('#rank-table >tbody>tr')

f = open('fifa_rank.csv', 'w', encoding='cp949',newline='')
wr = csv.writer(f)



for obj in fifa_rank_list :
    rank=[]
    rank.append(obj.find('td', {'class': 'fi-table__rank'}).text+'위')
    rank.append(obj.find('span', {'class': 'fi-t__nText'}).text)
    wr.writerow(rank)
    print(obj.find('td', {'class': 'fi-table__rank'}).text,'위 : ', obj.find('span', {'class': 'fi-t__nText'}).text )
    if obj.find('span', {'class': 'fi-t__nTri'}).text == 'KOR':
        print('한국 피파랭킹 : ' , obj.find('td', {'class': 'fi-table__rank'}).text,'위')
        break;
    #wr.writerow(obj.find.text)

f.close()
kfa_result = "https://www.kfa.or.kr/national/?act=nt_man&position=&s_idx=1619&search_val=2019&cursor=#cursor_location_sub"
kfa_result_html = requests.get(kfa_result)
soup = BeautifulSoup(kfa_result_html.content,"html.parser", from_encoding='utf=8')

#kfa_randk_list = kfa_result_html_list.select('#rank-table >tbody>tr')
#for obj in kfa_result_list :
#    if obj.find('span', {'class': 'fi-t__nTri'}).text == '경기결과':
date = soup.findAll('em')
for em in date:
    print(em.text)
    
divList=soup.findAll('div',attrs={'class':'result_info'})
##
for div in divList:
    korea=div.find('li',attrs={'class':'korea'})
    away=div.find('li',attrs={'class': 'away'})
    print(korea.text)
    print(away.text)
##


'''
koreaList = soup.findAll('li', attrs={'class':'korea'})
awayList = soup.findAll('li', attrs={'class':'away'})
print('시작')
for korea in koreaList:
    print(korea.text)
    koreaScore = korea.find('span')
    #print(koreaScore.text)
    print('한줄\n')


for away in awayList:
    print(away.text)
    print('한줄\n')
    awayScore = away.find('span')
    print(awayScore.text)
    print('한줄\n')
'''


client_id = 'Pin8Q7KyWNbYqMa3dUVF'
client_secret = 'A1pVDxSQmR'


#[CODE 1]
def getRequestUrl(url):    
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", "Pin8Q7KyWNbYqMa3dUVF")
    req.add_header("X-Naver-Client-Secret", "A1pVDxSQmR")
    
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getNaverSearch(node, srcText, start, display):    
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)
    
    url = base + node + parameters    
    responseDecode = getRequestUrl(url)   #[CODE 1]
    
    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

#[CODE 3]
def getPostData(post, jsonResult, cnt):    
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    pDate = datetime.datetime.strptime(post['pubDate'],  '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
    
    jsonResult.append({'cnt':cnt, 'title':title, 'description': description, 'org_link':org_link,   'link': link,   'pDate':pDate})
    
    return    

#[CODE 0]
def main():
    node = 'news'
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)  #[CODE 2]
    total = jsonResponse['total']
 
    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):         
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)  #[CODE 3]       
        
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)  #[CODE 2]
       
    print('전체 검색 : %d 건' %total)
    
    with open('./%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult,  indent=4, sort_keys=True,  ensure_ascii=False)
                        
        outfile.write(jsonFile)
        
    print("가져온 데이터 : %d 건" %(cnt))
    print ('%s_naver_%s.json SAVED' % (srcText, node))

    
    
if __name__ == '__main__':
    main()
