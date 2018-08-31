#stt 인식결과를 BigQuery에 저장한다.sample_rate_hertz
def saveBigQuery(speech_num, speech_cognition_type, stt_status, error_msg, result_text,
                 sample_rate_hertz, model, use_enhanced, interactionType, industryNaicsCodeOfAudio,
                 microphoneDistance, originalMediaType, recordingDeviceType, percent_similarity, audio_stream_time,
                 confidence, latency):
    print('============ start saveBigQuery ============')
    print('speech_num : ', speech_num)
    print('speech_cognition_type : ', speech_cognition_type)
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

if __name__ == '__main__':
    print('hello bigquery')
    saveBigQuery(1, '2', 1, '', '안녕하세요',
                 8000, '', False, 'DISCUSSION', '522291',
                 'NEARFIELD', 'AUDIO', 'PHONE_LINE', 100, '1:30',
                 0.920661211013794, 3.222222)
