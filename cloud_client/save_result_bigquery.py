from google.cloud import bigquery
import datetime

#stt 인식결과를 BigQuery에 저장한다.sample_rate_hertzstt_status
def saveBigQuery(speech_num, speech_cognition_type, stt_status, error_msg, result_text,
                 sample_rate_hertz, model, use_enhanced, interactionType, industryNaicsCodeOfAudio,
                 microphoneDistance, originalMediaType, recordingDeviceType, percent_similarity, audio_stream_time,
                 confidence, latency):
    print('============ start saveBigQuery ============')
    print('speech_num : ', speech_num)
    print('speech_cognition_type : ', speech_cognition_type)
    print('stt_status : ', stt_status)
    print('error_msg : ', error_msg)
    print('result_text : ', result_text)
    print('sample_rate_hertz : ', sample_rate_hertz)
    print('model : ', model)
    print('use_enhanced : ', use_enhanced)
    print('interactionType : ', interactionType)
    print('industryNaicsCodeOfAudio : ', industryNaicsCodeOfAudio)
    print('microphoneDistance : ', microphoneDistance)
    print('originalMediaType : ', originalMediaType)
    print('recordingDeviceType : ', recordingDeviceType)
    print('percent_similarity : ', percent_similarity)
    print('audio_stream_time : ', audio_stream_time)
    print('confidence : ', confidence)
    print('latency : ', latency)
    print('============ end saveBigQuery ============')

    # TODO(developer): Uncomment the lines below and replace with your values.
    client = bigquery.Client()
    dataset_id = 'gc_ml_lab'  # replace with your dataset ID
    # For this sample, the table must already exist and have a defined schema
    #table_id = 'stt_result_info$'+datetime.datetime.today().strftime('%Y%m%d')  # replace with your table ID
    table_id = 'stt_result_info_real'
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    # 누락된 변수선언
    stt_result_num = datetime.datetime.now().strftime('%m%d%H%M%S%f')

    recordingDeviceName = ''
    originalMimeType = 'audio/wav'
    obfuscatedId = ''
    audioTopic = '대출상담'
    enable_automatic_punctuation = False
    enable_word_time_offsets = False

    insert_dt = datetime.datetime.now()

    rows_to_insert = [
        (speech_num, stt_result_num, speech_cognition_type, stt_status, error_msg,
         result_text, sample_rate_hertz, model, use_enhanced, interactionType,
         industryNaicsCodeOfAudio, microphoneDistance, originalMediaType, recordingDeviceType, recordingDeviceName,
         originalMimeType, obfuscatedId, audioTopic, enable_automatic_punctuation, enable_word_time_offsets,
         percent_similarity, audio_stream_time, insert_dt, round(confidence, 3), round(latency, 3))]

    errors = client.insert_rows(table, rows_to_insert) # API request
    print('bigquery insert row error : ', errors)

if __name__ == '__main__':
    print('hello bigquery')
    saveBigQuery(1, '2', 1, '', '안녕하세요',
                 8000, '', False, 'DISCUSSION', '522291',
                 'NEARFIELD', 'AUDIO', 'PHONE_LINE', 100, '1:30',
                 0.92066, 3.2222)