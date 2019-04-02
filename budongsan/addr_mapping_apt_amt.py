import csv
import re

#아파트명
brand_apt_arr = ['푸르지오','레미안','래미안','이편한세상','E편한세상','E-편한세상','e편한세상','자이','더샵','더샵센트럴뷰','아이파크','롯데캐슬','힐스테이트','우성','코오롱하늘채','코오롱오투빌',
    '보람','쌍용예가','동보','태영','데시앙','주공','청구','리센츠','더하임','현대홈타운','현대','한양홈타운','한양수자인','한양','신동아','그랑시아','파크데일','삼성홈타운','삼성','신트리',
    '금호베스트빌','경남','경남아너스빌','남산타운','상동뜨란채','가람','엔파크','일성인포','극동스타클래스','후곡마을','대동','대우디오빌플러스','광명','성지','휴먼시아','파크타운서안','신시가지',
    '하늘도시우미린','궁전','신일유토빌플러스','숲속마을','광장','성원상떼빌','해태','삼환','햇빛마을','EG the','강변뜨란채','국제파크','상아','가람마을','센트레빌','두산위브','두산','서희아리채','소만마을'
]

def execute_addr_amt_job(file_path):
    print('=== execute_addr_amt_job start ===')
    #1. 고객주소 CSV 파일을 읽어들여 튜플에 담는다.
    addr_tuple = get_customer_addr_data(file_path)
    addrset_list = []
    print('addr_tuple : ', addr_tuple)

    for key, values in addr_tuple.items():
        #print('key : ', key)
        #print('values : ', values)
        for customer_addr in values:
            #print('customer_addr : ', customer_addr)
            customer_addr_arr = parseCustomerAddrToArr(str(customer_addr))
            #print('customer_addr_arr : ', customer_addr_arr)
            addrset_list.append(customer_addr_arr)

    #addr_tuple 튜플에 고객주소 배열을 담는다.
    print('addrset_list : ', addrset_list)


    print('=== execute_addr_amt_job start ===')

#고객 주소를 파싱하여 배열에 담는다.
#[시도, 시구, 도로명, 상세주소, 동리, 아파트명, 아파트 구분]
def parseCustomerAddrToArr(customer_addr):
    #주소의 () 안에 공백이 있다면 제거해서 다시 고객주소 변수에 담는다.
    customer_addr = customer_addr[0 : customer_addr.find('(')] + customer_addr[customer_addr.find('(') : len(customer_addr)].replace(' ', '')
    addr_arr = customer_addr.split(' ')
    result_arr = []
    sido = ''
    sigu = ''
    load_name = ''
    detail_addr = ''
    dongri = ''
    apt_name = ''
    only_apt_name = '' #아파트명만
    apt_danji = '' # 아파트단지
    apt_cha = '' # 아파트차수
    apt_dong = '' # 아파트동
    apt_ho = '' # 아파트호
    apt_town = '' #아파트 마을명
    building_name_flag = False

    for addr_bit in addr_arr:
        if sido == '':
            #시도명 표준화 서울특별시 -> 서울, 세종특별자치시 -> 세종
            sido = convert_sido_standard(addr_bit)
        else:
            if sigu == '':
                if sido.find('세종') > -1:
                    sigu = ' ' #세종시는 시구 공백처리
                else:
                    sigu =  addr_bit
            else:
                if load_name == '' and dongri == '':
                    #경기도의 경우 도,시,구 주소 체계   또는   도,시,면      또는 도,시,읍
                    if addr_bit[len(addr_bit) - 1: len(addr_bit)] == '구' or addr_bit[len(addr_bit) - 1: len(addr_bit)] == '면' or addr_bit[len(addr_bit) - 1: len(addr_bit)] == '읍':
                        sigu = sigu + ' ' + addr_bit
                    else:
                        if addr_bit[len(addr_bit)-1 : len(addr_bit)] == '길' or addr_bit[len(addr_bit)-1 : len(addr_bit)] == '로':
                            load_name = addr_bit
                        else:
                            load_name = ' '
                            #도로명이 없으면 동,리를 찾는다.
                            if addr_bit[len(addr_bit)-1 : len(addr_bit)] == '동' or addr_bit[len(addr_bit)-1 : len(addr_bit)] == '리':
                                dongri = addr_bit
                            else:
                                dongri = ' '
                else:
                    apt_addr_start_idx = addr_bit.find('(')
                    apt_addr_end_idx = addr_bit.find(')')
                    comma_idx = addr_bit.find(',')
                    #상세주소
                    if apt_addr_start_idx == -1:
                        detail_addr = detail_addr + ' ' + addr_bit
                    else:
                        detail_addr = detail_addr + ' ' + addr_bit[0 : apt_addr_start_idx]

                        # 동리 변수가 비어있으면
                        if dongri == '':
                            if comma_idx > -1:
                                dongri = addr_bit[apt_addr_start_idx + 1: comma_idx]
                            else:
                                dongri = addr_bit[apt_addr_start_idx + 1: apt_addr_end_idx]
                        if comma_idx > -1:
                            #()안에 ,가 있으면 아파트명을 변수에 담는다.
                            apt_name = addr_bit[comma_idx+1 : apt_addr_end_idx]

                    # 브랜드 아파트를 체크하여 브랜드 아파트이면 아파트명 변수에 담는다.
                    if apt_name == '' or apt_name == ' ':
                        apt_name = check_brand_apt(addr_bit)
                        #상세주소에서 아파트명을 제거한다.
                        if apt_name != ' ':
                            detail_addr = detail_addr.replace(apt_name, '')

    if apt_name != '' and apt_name != ' ':
        # 아파트 , 타운하우스 키우드 제거
        only_apt_name = apt_name.replace('아파트', '') #.replace('타운하우스', '')

        # 아파트단지 처리
        if len(re.findall('\d+단지', only_apt_name)) > 0:
            apt_danji = re.findall('\d+단지', only_apt_name)[0]
            only_apt_name = only_apt_name.replace(apt_danji, '')

        # 아파트차수 차수 처리(아파트명에 차수 포함 시)
        if len(re.findall('\d+차', only_apt_name)) > 0:
            apt_cha = re.findall('\d+차', only_apt_name)[0]
            only_apt_name = only_apt_name.replace(apt_cha, '')

        # 아파트차수 차수 처리(상세주소에 차수 포함 시)
        if len(re.findall('\d+차', detail_addr)) > 0:
            apt_cha = re.findall('\d+차', detail_addr)[0]
            detail_addr = detail_addr.replace(apt_cha, '')

        #아파트 마을명
        if len(re.findall('\w+마을', only_apt_name)) > 0:
            apt_town = re.findall('\w+마을', only_apt_name)[0]
            only_apt_name = only_apt_name.replace(apt_town, '')

        # 아파트동 처리
        if len(re.findall('\d+동', detail_addr)) > 0:
            apt_dong = re.findall('\d+동', detail_addr)[0]

        # 아파트호 처리
        if len(re.findall('\d+호', detail_addr)) > 0:
            apt_ho = re.findall('\d+호', detail_addr)[0]

        #이편한세상 처리
        only_apt_name = process_daerim_e_apt(only_apt_name)

        #아파트명에서 시도,구군, 동이름 제거 -- 사직2차쌍용예가 처리를 위해 필요
        only_apt_name = apt_name_cut_areaname(only_apt_name, sido, sigu, dongri)

        #아파트명이 모두 필터링 되고 없으면, 아파트마을명을 아파트명 지정
        if only_apt_name == '':
            only_apt_name = apt_town
        
        building_name_flag = True
    else:
        only_apt_name = ' '
        apt_danji = ' '
        apt_cha = ' '
        apt_town = ' '
        apt_dong = ' '
        apt_ho = ' '

    ##[시도, 시구, 도로명, 상세주소, 동리, 원본_아파트명, 아파트명, 단지, 차수, 아파트동, 아파트호, 아파트마을명, 아파트 구분]
    result_arr = [customer_addr, sido, sigu, load_name, detail_addr.strip(), dongri, apt_name, only_apt_name, apt_danji, apt_cha, apt_dong, apt_ho, apt_town, building_name_flag]

    print(result_arr)

    return result_arr

# 아파트명에서 시도,구군, 동이름 제거 -- 사직2차쌍용예가 처리를 위해 필요
def apt_name_cut_areaname(only_apt_name, sido, sigu, dongri):
    dong_name = dongri[0 : len(dongri)-1]
    sido_name = sido[0: len(sido) - 1]

    #아파트명에 동명 포함 시 제거
    if only_apt_name.find(dong_name) > -1 and only_apt_name != dongri and len(only_apt_name) > len(dong_name):
        only_apt_name = str(only_apt_name).replace(dong_name, '')

    # 아파트명에 시도명 포함 시 제거
    if only_apt_name.find(sido) > -1 and only_apt_name != sido and len(only_apt_name) > len(sido):
        only_apt_name = str(only_apt_name).replace(sido, '')

    sigu_arr = sigu.split(' ')
    # 아파트명에 시구명의 시 포함 시 제거 (용인시 수지구 -> 용인시)
    if len(sigu_arr) > 0:
        si_name = sigu_arr[0][0: len(sigu_arr[0]) - 1]
        if only_apt_name.find(si_name) > -1 and only_apt_name != sigu_arr[0] and len(only_apt_name) > len(si_name):
            only_apt_name = str(only_apt_name).replace(si_name, '')

    # 아파트명에 시구명의 구 포함 시 제거 (용인시 수지구 -> 수지구)
    if len(sigu_arr) > 1:
        gu_name = sigu_arr[1][0: len(sigu_arr[1]) - 1]
        if only_apt_name.find(gu_name) > -1 and only_apt_name != sigu_arr[1] and len(only_apt_name) > len(gu_name):
            only_apt_name = str(only_apt_name).replace(gu_name, '')

    return only_apt_name

#시도 표준화 (EX. 세종특별자치시 -> 세종)
def convert_sido_standard(sido):
    sido_short_name = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '제주',
                       '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남']
    sido_middle_name = ['서울시', '부산시', '대구시', '인천시', '광주시', '대전시', '울산시', '세종시', '제주도',
                        '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도']
    sido_long_name = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시', '제주특별자치도',
                      '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도']

    #시도 풀네임 이면 short name으로 변환
    for idx, sido_long in enumerate(sido_long_name):
        if sido_long == sido:
            return sido_short_name[idx]

    # 시도 중간네임 이면 short name으로 변환
    for idx, sido_middle in enumerate(sido_middle_name):
        if sido_middle == sido:
            return sido_short_name[idx]

    return sido


# 아파트명 대림이편한세상, 이편한세상, E편한세상, e편한세상, 'E-편한세상','e-편한세상' , E편한세상 --> 이편한세상
def process_daerim_e_apt(only_apt_name):
    dearim_e_brand_arr = ['대림이편한세상', '대림이-편한세상', '대림E편한세상', '대림E-편한세상', '대림e-편한세상', '대림e편한세상',
                          '이편한세상', '이-편한세상', 'E편한세상', 'E-편한세상', 'e-편한세상', 'e편한세상']

    for e_str in dearim_e_brand_arr:
        if only_apt_name.find(e_str) > -1:
            return only_apt_name.replace(e_str, 'E편한세상')

    return only_apt_name

#상세주소를 체크하여 브랜드 아파트면 아파트명을 리턴한다.
def check_brand_apt(addr_str):
    result_apt_name = ''

    for bran_apt_name in brand_apt_arr:
        if addr_str.find(bran_apt_name) > -1:
            #주소에서 아파트명만 찾아 return 한다.
            if addr_str.find(bran_apt_name) > -1:
                result_apt_name = addr_str
                return result_apt_name

    if addr_str.find('아파트') > -1:
        result_apt_name = addr_str
    else:
        result_apt_name = ' '

    return result_apt_name

#주소에 check_str가 포함되어 있는지 체크한다.
def check_inclusion(ori_addr , check_str):
    if check_str in ori_addr:
        return True
    else:
        return False

#고객주소 CSV 파일을 읽어들여 튜플에 담는다.
def get_customer_addr_data(file_path):
    # strip 함수는 문자열 양끝의 \n, ' '를 삭제한다.
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {key.strip():[value.strip()] for key,value in reader.__next__().items()}

        for line in reader:
            for key,value in line.items():
                key = key.strip()
                data[key].append(value.strip())
    return data

if __name__=="__main__":
    print('=== customer addr mapping apt amt start ===')
    file_path = 'C:/Users/웰컴저축은행/Desktop/웰컴저축은행/개발관련/빅데이터플랫폼/아파트실거래가/주소.csv'
    execute_addr_amt_job(file_path)
    print('=== customer addr mapping apt amt end ===')