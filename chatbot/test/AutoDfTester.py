import uuid
#import dialogflow_v2 as dialogflow
import dialogflow_v2beta1 as dialogflow
# Imports the Google Cloud client library
import chatbot.test.saveResultInfoBigQuery as save_result_bigquery

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    return_list = []

    #import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        # Enable sentiment analysis
        sentiment_config = dialogflow.types.SentimentAnalysisRequestConfig(
            analyze_query_text_sentiment=True)

        # Set the query parameters with sentiment analysis
        query_params = dialogflow.types.QueryParameters(
            sentiment_analysis_request_config=sentiment_config)

        response = session_client.detect_intent(
            session=session, query_input=query_input,
            query_params=query_params) #감정분석 옵션이 붙는 경우만

        query = text
        query_text = response.query_result.query_text
        response_id = response.response_id
        #query_result = response.query_result
        intent_name = response.query_result.intent.display_name
        intent_detection_confidence = response.query_result.intent_detection_confidence
        result_msg = response.query_result.fulfillment_text
        sentiment_score = response.query_result.sentiment_analysis_result.query_text_sentiment.score

        result_dic = {
            'query' : query,
            'query_text': query_text,
            'response_id': response_id,
            'intent_name': intent_name,
            'intent_detection_confidence': intent_detection_confidence,
            'result_msg': result_msg,
            'sentiment_score': sentiment_score}
        return_list.append(result_dic)

        print('=' * 20)
        print('query : ', query)
        print('query_text : ', query_text)
        print('response_id : ', response_id)
        #print('query_result : ', query_result)
        print('intent_name : ', intent_name)
        print('intent_detection_confidence : ', intent_detection_confidence)
        print('result_msg : ', result_msg)
        print('sentiment_score : ', sentiment_score)


    #BigQuery에 저장한 정보를 list형 변수에 담아 return
    return return_list

if __name__ == '__main__':
    file_path = 'C:/df/testfile/'
    #file_name_list = ['테스트케이스1.txt','테스트케이스2.txt', '테스트케이스3.txt', '테스트케이스4.txt']
    #file_name_list = ['테스트케이스2.txt']
    file_name_list = ['test.txt']

    for file_name in file_name_list:
        file_full_path = file_path + file_name

        print('============ ' + file_full_path + ' processing start!! ============')
        with open(file_full_path) as f:
            lines = f.readlines()

            return_list = detect_intent_texts('ml-lab-207601', uuid, lines, 'ko-KR')

            #응답 메시지에서 주요한 정보들을 BigQuery에 저장.
            print(len(return_list))
            save_result_bigquery.saveBigQuery(return_list, file_name)

        print('============ ' + file_full_path + ' processing end!! ============')
