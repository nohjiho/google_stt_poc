from google.cloud import bigquery
import datetime

def saveBigQuery(return_list, file_name):
    print('============ start saveBigQuery ============')

    # TODO(developer): Uncomment the lines below and replace with your values.
    client = bigquery.Client()
    dataset_id = 'gc_ml_lab'  # replace with your dataset ID
    # For this sample, the table must already exist and have a defined schema
    #table_id = 'stt_result_info$'+datetime.datetime.today().strftime('%Y%m%d')  # replace with your table ID
    table_id = 'df_result_info'
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    # 누락된 변수선언
    df_result_num = datetime.datetime.now().strftime('%m%d%H%M%S%f')
    insert_dt = datetime.datetime.now()

    rows_to_insert = []
    for save_info in return_list:
        print('============ append save ifo ' + save_info['query'] + ' start !! ============')
        print('df_result_num : ', df_result_num)
        print('response_id : ', save_info['response_id'])
        print('intent_name : ', save_info['intent_name'])
        print('file_name : ', file_name)
        print('query : ', save_info['query'])
        print('query_text : ', save_info['query_text'])
        print('intent_detection_confidence : ', save_info['intent_detection_confidence'])
        print('result_msg : ', save_info['result_msg'])
        print('sentiment_score : ', save_info['sentiment_score'])
        print('right_answer_flaq : ', '0')
        print('insert_dt : ', insert_dt)
        print('============ append save ifo ' + save_info['query'] + ' end !! ============')
        rows_to_insert.append(
            (df_result_num,
              save_info['response_id'],
              save_info['intent_name'],
              file_name,
              save_info['query'],
              save_info['query_text'],
              save_info['intent_detection_confidence'],
              save_info['result_msg'],
              save_info['sentiment_score'],
              '0',
              insert_dt))

    print('rows_to_insert : ', rows_to_insert)
    errors = client.insert_rows(table, rows_to_insert) # API request
    print('bigquery insert row error : ', errors)

    print('============ end saveBigQuery ============')

if __name__ == '__main__':
    print('hello bigquery')
    saveBigQuery( [
        {'query': '대출상환금이 이중으로 출금되었습니다. 반환부탁드립니다.\n',
         'query_text': '대출상환금이 이중으로 출금되었습니다. 반환부탁드립니다.\n',
         'response_id': 'b3823edc-60d2-4cf3-ae19-4253e721fb46',
         'intent_name': '00390000-FAQ-double-payment',
         'intent_detection_confidence': 0.800000011920929,
         'result_msg': '대출 상환금 이중출금의 경우, 이중출금 익일 오전 중(12시 이전)으로 자동 반환처리됩니다.| 예적금 자동이체의 이중출금의 경우, 이중출금반환이 불가한 점 양해 부탁드립니다.',
         'sentiment_score': 0.30000001192092896},
        {'query': '신용조회상 불량정보가 있었는데 대출이 될까요?',
         'query_text': '신용조회상 불량정보가 있었는데 대출이 될까요?',
         'response_id': '54792701-4c10-44de-9498-b0238ec4594a',
         'intent_name': '00270000-FAQ-BadCredit', 'intent_detection_confidence': 0.5,
         'result_msg': '당행은 신용등급 외 소득 및 채무상환능력 등의 종합적인 기준에 의해 대출 상담이 진행되며| 신용등급이 낮다고 대출이 불가하진 않습니다.| | 대출신청!을 입력하시면, 대출상담 페이지로 이동합니다.',
         'sentiment_score': -0.6000000238418579}
    ])