# coding=utf-8
#
# 아파트매매 실거래자료
#

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
    
import pandas as pd
from bs4 import BeautifulSoup
#from html_table_parser import parser_functions as parser
import html_table_parser
import sys
import os
#arg values
yyyymm = sys.argv[1]    #데이터 기준 년월
la_cd = sys.argv[2]     #행정동코드
 
def collect_land_sale(ym,lawd_cd):
 
    #공공데이터포털에서 부여받은 키 셋팅
    API_KEY = "P5acAromyrPSOLQS%2BO2PgQAm0c81H%2FvqYd0r1fe9ApwdDzpCy8bZXbO91E319%2FuU%2Fzxq6vsgfuCVpk228aWh2A%3D%3D"
    #url="http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcLandTrade"
    url="http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade"
 
    url=url+"?LAWD_CD="+lawd_cd+"&DEAL_YMD="+ym+"&serviceKey="+API_KEY
 
    resultXML = urlopen(url)
    result = resultXML.read()
    xmlsoup = BeautifulSoup(result, 'lxml-xml')
 
    #가져올 항목이 item에 있음
    te=xmlsoup.findAll("item")
    df=pd.DataFrame()
 
    for t in te:
        price = t.find("거래금액").text
        buildyear = t.find("건축년도").text
        year=t.find("년").text
        month=t.find("월").text
        day=t.find("일").text
        dong=t.find("법정동").text
        apt=t.find("아파트").text
        size = t.find("전용면적").text
        jibun = t.find("지번").text
        lawd_cd=t.find("지역코드").text
        floor=t.find("층").text
 
        #pandas DataFrame으로 변환
        temp = pd.DataFrame(([[price,buildyear,year,month,day,dong,apt,size,jibun,lawd_cd,floor]]),
                            columns=["price","buildyear","year","month","day","dong","apt","size","jibun","lawd_cd","floor"])
        df=pd.concat([df,temp])
 
    df=df.reset_index(drop=True)
 
    # output.csv 저장 (파일 없으면 새로 생성, 존재하면 기존 파일에 내용 추가)
    if not os.path.isfile('output.csv'):
        df.to_csv('output.csv', mode='w', encoding='utf-8')
    else:
        df.to_csv('output.csv', mode='a', encoding='utf-8', header=False)
 
if __name__=="__main__":
    data=collect_land_sale(yyyymm, la_cd)
