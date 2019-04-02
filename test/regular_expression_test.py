import re

text = '후곡마을10단지현대아파트'
danji = ''

text = text.replace('아파트', '')
print('아파트 키워드 제거 : ', text)
danji = re.findall('\d+단지', text)[0]
print('danji : ', danji)
text = text.replace(danji, '')
print('단지 제거 : ', text)

apt_town = re.findall('\w+마을', text)[0]
print('apt_town : ', apt_town)




