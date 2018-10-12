# -*- coding : utf-8 -*-
#easy_install --upgrade Flask
from flask import Flask, request, make_response, jsonify
import requests as requests
import json as json

ERROR_MESSAGE = '오류메시지'

app = Flask(__name__)

#웹훅 펑션
@app.route('/', methods=['POST'])
def webhook():
    #return "Hello Webhook"
    #on_json_loading_failed() 재정의(json parsing 오류처리)
    request.on_json_loading_failed = on_json_loading_failed_return_dict

    # 액션 구함
    req = request.get_json(force=True)
    action = req['result']['action']

    print('req : ', req)
    print('action : ', action)

    #액션 처리
    if action == 'category_info':
        category_name = req['result']['parameters']['category_type']
        print('category_name : ', category_name)
        answer = process_catetory_info(category_name)
    else:
        answer = '액션 없음. error'

    res = {'speech' :  answer}
    return jsonify(res)

#키보드 처리
@app.route('/keyboard', methods=['POST'])
def keyboard():
    res = {
        'type' : 'buttons' ,
        'buttons' : ['대화하기']
    }
    return jsonify(res)

#메시지 처리
@app.route('/message', methods=['POST'])
def message():
    # on_json_loading_failed() 재정의(json parsing 오류처리)
    request.on_json_loading_failed = on_json_loading_failed_return_dict
    #메시지 받기
    req = request.get_json()
    user_key = req['user_key']
    content = req['content']

    if len(user_key) > 1 or len(content) > 1:
        answer = ERROR_MESSAGE

    #답변 구함
    answer = get_answer(content, user_key)

    #메시지 설정
    res = {
        'message' : {'text' : answer}
    }

    return jsonify(res)

#답변 함수
def get_answer(text, user_key):
    #Dialogflow에 요청
    data_send = {
        'lang' : 'ko' ,
        'query' : text,
        'sessionId' : user_key ,
        'timezone' : 'Asia/Seoul'
    }

    data_header = {
        'Content-Type' : 'application/json; charset=utf-8' ,
        'Authorization' : '9b59af7a02854c7788524b3ed798bad3' # Client access Token
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20181012'

    res = requests.post(dialogflow_url ,
                        data=json.dumps(data_send) ,
                        headers=data_header)

    #대답처리
    if res.status_code != requests.codes.ok:
        return ERROR_MESSAGE

    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech']

    return answer

#오류처리 함수
def on_json_loading_failed_return_dict(e):
    print('on_json_loading_failed_return_dict : ', e)
    return {}

def process_catetory_info(category_name):
    if category_name == u'홈페이지/앱이용':
        answer = '<Photo>https://www.welcomebank.co.kr/web/ibn/img/main/logo_intro.png</Photo>'
        answer += '웰컴디지털뱅크 홈페이지/앱이용 관련 이용 문의를 할 수 있습니다.'
        answer += '홈페이지/앱이용 질문을 선택하거나 직접 질문을 입력 해 주세요.'
    elif category_name == u'예적금':
        answer = '웰컴디지털뱅크 예적금 관련 이용 문의를 할 수 있습니다.'
        answer += '예적금 질문을 선택하거나 직접 질문을 입력 해 주세요.'
    elif category_name == u'대출':
        answer = '<Photo>https://www.welcomebank.co.kr/web/ibn/img/main/logo_intro.png</Photo>'
        answer += '웰컴디지털뱅크 대출 관련 이용 문의를 할 수 있습니다.'
        answer += '대출 질문을 선택하거나 직접 질문을 입력 해 주세요.'
    elif category_name == u'카드':
        answer = '<Photo>https://www.welcomebank.co.kr/web/ibn/img/main/logo_intro.png</Photo>'
        answer += '웰컴디지털뱅크 카드 관련 이용 문의를 할 수 있습니다.'
        answer += '카드 질문을 선택하거나 직접 질문을 입력 해 주세요.'
    elif category_name == u'환전':
        answer = '<Photo>https://www.welcomebank.co.kr/web/ibn/img/main/logo_intro.png</Photo>'
        answer += '웰컴디지털뱅크 환전 관련 이용 문의를 할 수 있습니다.'
        answer += '환전 질문을 선택하거나 직접 질문을 입력 해 주세요.'
    elif category_name == u'보안':
        answer = '<Photo>https://www.welcomebank.co.kr/web/ibn/img/main/logo_intro.png</Photo>'
        answer += '웰컴디지털뱅크 보안 관련 이용 문의를 할 수 있습니다.'
        answer += '보안 질문을 선택하거나 직접 질문을 입력 해 주세요.'
    elif category_name == u'기타':
        answer = '<Photo>https://www.welcomebank.co.kr/web/ibn/img/main/logo_intro.png</Photo>'
        answer += '웰컴디지털뱅크 기타 관련 이용 문의를 할 수 있습니다.'
        answer += '기타 질문을 선택하거나 직접 질문을 입력 해 주세요.'

    return answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5110, threaded=True)