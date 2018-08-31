#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
"""Google Cloud Speech API sample application using the REST API for async
batch processing.
Example usage:
    python transcribe_async.py resources/audio.raw
    python transcribe_async.py gs://cloud-samples-tests/speech/vr.flac
"""
#긴 오디오 파일 인식(비동기 방식)
#실행 시 parameters 입력 : C:/Users/웰컴저축은행/workspace/google_stt_lab\resources\샘플1_1분.wav
#원격지에서는 google storage 경로 입력
#gs://dlab_ml/speech/ref/샘플_1_개인정보삭제.wav
import argparse
import io
import sys
import cloud_client.transcribe_async as long_speech
import cloud_client.save_result_bigquery as save_result_bigquery

# [START speech_transcribe_async_gcs]
def execute():
    #1. 구글 스토리지의 파일 리스트
    files_gs_path = [(1,'gs://dlab_ml/speech/ref/샘플_1_개인정보삭제.wav'),
                     (2, 'gs://dlab_ml/speech/ref/샘플_2_개인정보삭제.wav'),
                     (3, 'gs://dlab_ml/speech/ref/샘플_3_개인정보삭제.wav'),
                     (4, 'gs://dlab_ml/speech/ref/샘플_4_개인정보삭제.wav'),
                     (5, 'gs://dlab_ml/speech/ref/샘플_5_개인정보삭제.wav'),
                     (6, 'gs://dlab_ml/speech/ref/샘플_6_개인정보삭제.wav'),
                     (7, 'gs://dlab_ml/speech/ref/샘플_7_개인정보삭제.wav'),
                     (8, 'gs://dlab_ml/speech/ref/샘플_8_개인정보삭제.wav'),
                     (9, 'gs://dlab_ml/speech/ref/샘플_9_개인정보삭제.wav'),
                     (10, 'gs://dlab_ml/speech/ref/샘플_10_개인정보삭제.wav')]

    # 샘플비율 헤르츠
    sample_rate_hertzs = [(1, 6000),
                     (2, 8000),
                     (3, 10000)]

    #오디오 사용 사례
    interactionTypes = [(1, 'INTERACTION_TYPE_UNSPECIFIED'),
                          (2, 'DISCUSSION'),
                          (3, 'PRESENTATION')]
    #오디오 산업 카테고리
    industryNaicsCodeOfAudios = [(1, '522291'),
                          (3, 'PRESENTATION')]

    #스피커에서 마이크 까지의 거리
    microphoneDistances =  [(1, 'MICROPHONE_DISTANCE_UNSPECIFIED'),
                          (2, 'NEARFIELD'),
                          (3, 'MIDFIELD')]

    # 오디오의 원본 오디오 또는 비디오 중 하나
    originalMediaTypes = [(1, 'ORIGINAL_MEDIA_TYPE_UNSPECIFIED'),
                           (2, 'AUDIO')]

    #오디오 캡쳐 장치 종류
    recordingDeviceTypes = [(1, 'RECORDING_DEVICE_TYPE_UNSPECIFIED'),
                          (2, 'SMARTPHONE'),
                          (3, 'PHONE_LINE')]

    # 2. 파일 수 만큼 loop를 돌려 긴오디오 인식을 수행한다.  (메터 데이터 인식 제외)
    for (speech_num, file_gs_path) in files_gs_path:
        print(' ============ start ', file_gs_path, ' ===============')
        tuple_result_msg = ()
        result_msg = ''
        except_msg = ''
        confidence = 0
        stt_status = 1
        try:
            #2-2. 긴 오디오 파일 인식 결과 가져오기
            tuple_result_msg = long_speech.transcribe_gcs(file_gs_path)
            result_msg = tuple_result_msg[0]
            confidence = tuple_result_msg[1]
        except:
            stt_status = -1
            #TODO : 오류가 발생하면 except_msg 변수에 담는다.
            except_msg = sys.exc_info()
            print("Unexpected error:", except_msg)
            #오류 무시
            pass
        finally:
            print('result_msg : ', result_msg)
            #2-3.빅쿼리에 결과 저장
            try:
                save_result_bigquery.saveBigQuery(speech_num, '2', stt_status, except_msg, result_msg,
                     8000, '', False, 'DISCUSSION', '522291',
                     'NEARFIELD', 'AUDIO', 'PHONE_LINE', 100, '1:30',
                      confidence)
            except:
                except_msg = sys.exc_info()
                print("Unexpected error:", except_msg)
                pass
            print(' ============ end ', file_gs_path, ' ===============')

    #3. 파일 수 만큼 loop를 돌려 긴오디오 인식을 수행한다.(메터 데이터 설정 인식)



# [END speech_transcribe_async_gcs]

if __name__ == '__main__':
    execute()