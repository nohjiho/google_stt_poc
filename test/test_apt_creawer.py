# -*- coding: utf-8 -*-

import requests
import json
import logging

URL = "http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do"

param = {
    'menuGubun': 'A',
    'p_apt_code': 20064683,
    'p_house_cd': 1,
    'p_acc_year': 2018
}

header = {
    'Referer': 'http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND'
}

logging.basicConfig(level=logging.INFO)

resp = requests.get(URL, params=param, headers=header)
if resp.status_code != 200:
    logging.error('invalid status: %d' % resp.status)
    exit

data = json.loads(resp.text)
for item in data['result']:
    if item['BLDG_AREA'] < 80 or item['BLDG_AREA'] > 85:
        continue
    logging.info('%02s월 %02s층 %s만원' % (item['DEAL_MM'], item['APTFNO'], item['SUM_AMT']))