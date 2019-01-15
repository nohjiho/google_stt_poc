# -*- coding : utf-8 -*-
# easy_install --upgrade Flask
from flask import Flask, request, make_response, jsonify
import requests as requests
import json as json
import sys
import uuid

ERROR_MESSAGE = '오류메시지'

app = Flask(__name__)


# 웹훅 펑션
@app.route('/', methods=['GET', 'POST'])
# @app.route('/')
def webhook():
    # return "Hello Webhook"
    # on_json_loading_failed() 재정의(json parsing 오류처리)
    request.on_json_loading_failed = on_json_loading_failed_return_dict

    # 액션 구함
    req = request.get_json(force=True)
    action = req['result']['action']

    print('req : ', req)
    print('action : ', action)

    # 액션 처리
    if action == 'category_info':
        category_name = req['result']['parameters']['category_type']
        print('category_name : ', category_name)
        answer = process_catetory_info(category_name)
    else:
        answer = '액션 없음. error'

    res = {'speech': answer}
    return jsonify(res)


@app.route('/friend/test')
def friend_test():
    print('=== friend_test ===')


@app.route('/chat_room/test')
def chat_room_test():
    print('=== chat room test ===')


# 키보드 처리
# @app.route('/keyboard')
@app.route('/keyboard', methods=['GET', 'POST'])
def keyboard():
    res = {
        'type': 'buttons',
        'buttons': ['대화하기']
    }
    return jsonify(res)


# 메시지 처리
@app.route('/message', methods=['POST'])
def message():
    print('start message!!')
    try:
        # on_json_loading_failed() 재정의(json parsing 오류처리)
        request.on_json_loading_failed = on_json_loading_failed_return_dict

        print('request.get_json() : ', request.get_json())
        # 메시지 받기
        req = request.get_json()
        user_key = req['user_key']
        content = req['content']

        print('req : ', req)
        print('user_key : ', user_key)
        print('content : ', content)

        if len(user_key) < 1 or len(content) < 1:
            answer = ERROR_MESSAGE

        # 답변 구함 api version v1
        # answer = get_answer(content, user_key)

        # 답변 구함 api version v2
        answer = get_answer_v2(content, user_key)

        # answer_message = "\\n".join(answer.splitlines())
        answer_intent_name = answer[0]
        answer_message = answer[1].replace('| ', '\n')
        # answer_message = answer[1]

        print('intent_name : ', answer_intent_name)
        print('answer_message : ', answer_message)

        print('find : ', answer_message[1].find('대출신청 진행을 위해 약관 동의를 해주세요.'))
        # 메시지 설정
        if answer_intent_name == 'Default Welcome Intent':
            res = {
                'message': {
                    'text': answer_message,
                    'photo': {
                        'url': 'http://35.200.52.162:5110/static/intro.jpg',
                        'width': 640,
                        'height': 480
                    }
                }
            }
        else:
            res = {
                'message': {'text': answer_message}
            }
        print('res : ', res)
    except:
        except_msg = sys.exc_info()
        print("Unexpected error:", except_msg)

    jsonify_res = jsonify(res)

    print('jsonify_res : ', jsonify_res)

    return jsonify_res


def get_answer_v2(text, user_key):
    session_id = str(uuid.uuid4())
    project_id = 'ml-lab-207601'
    language_code = 'ko'

    result_text = ''

    print('text', text)
    print('user_key', user_key)

    # easy_install --upgrade dialogflow
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    print('text_input', text_input)

    query_input = dialogflow.types.QueryInput(text=text_input)

    print('query_input', query_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('response', response)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

    result_text = response.query_result.fulfillment_text
    query_text = response.query_result.query_text
    intent_name = response.query_result.intent.display_name

    print('response : ', response)
    print('query_text : ', query_text)
    print('result_text : ', result_text)
    print('intent_name : ', intent_name)

    result_arr = [intent_name, result_text]

    return result_arr


# 오류처리 함수
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
    app.run(host='0.0.0.0', port=5110, threaded=True)  # 5110
