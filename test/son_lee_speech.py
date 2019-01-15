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
import time
import cloud_client.transcribe_async as long_speech
import cloud_client.beta_snippets as beta_snippets
import cloud_client.save_result_bigquery as save_result_bigquery

#1. 구글 스토리지의 파일 리스트
files_gs_path = [(12, 'gs://dlab_ml/speech/ref/샘플_12_개인정보삭제.wav', '2:36'),
        (13, 'gs://dlab_ml/speech/ref/샘플_13_개인정보삭제.wav', '2:20'),
        (14, 'gs://dlab_ml/speech/ref/샘플_14_개인정보삭제.wav', '2:04')
        ]

sample_rate_hertz = 44100 #8000

# [START execute]
def execute():
    # 2. 파일 수 만큼 loop를 돌려 긴오디오 인식을 수행한다.  (메터 데이터 인식 제외)
    #excuteLongAudio()

    print('files_gs_path : ', files_gs_path)

    #3. 파일 수 만큼 loop를 돌려 긴오디오 인식을 수행한다.(메터 데이터 설정 인식)
    executeMetaLongAudio()
# [END execute]

#파일 수 만큼 loop를 돌려 긴오디오 인식을 수행한다.  (메터 데이터 인식 제외)
def excuteLongAudio():
    for (speech_num, file_gs_path, stream_time) in files_gs_path:
        print(' ============ start ', file_gs_path, ', ', sample_rate_hertz, ' ===============')
        tuple_result_msg = ()
        result_msg = ''
        except_msg = ''
        confidence = 0
        stt_status = 1
        latency = 0
        try:
            start_time = time.time()
            print('start_time : ', start_time)

            # 2-2. 긴 오디오 파일 인식 결과 가져오기
            tuple_result_msg = long_speech.transcribe_gcs_return(file_gs_path)

            end_time = time.time()
            latency = end_time - start_time
            print('end_time : ', end_time)
            print('latency : ', latency)
            result_msg = tuple_result_msg[0]
            confidence = tuple_result_msg[1]
        except:
            stt_status = -1
            #오류가 발생하면 except_msg 변수에 담는다.
            except_msg = sys.exc_info()
            print("Unexpected error:", except_msg)
            #오류 무시
            pass
        finally:
            print('result_msg : ', result_msg)
            #2-3.빅쿼리에 결과 저장
            try:
                save_result_bigquery.saveBigQuery(speech_num, '2', stt_status, except_msg, result_msg,
                                                  sample_rate_hertz, '', False, '', '',
                                                  '', '', '', 0, stream_time,
                                                  confidence, latency)
            except:
                except_msg = sys.exc_info()
                print("Unexpected error:", except_msg)
                pass
            finally:
                print(' ============ end ', file_gs_path, ', ', sample_rate_hertz, ' ===============')

def executeMetaLongAudio():
    import google.cloud.speech_v1p1beta1 as speech
    # 오디오 사용 사례
    #INTERACTION_TYPE_UNSPECIFIED : 사용 사례가 알려지지 않았거나 아래의 다른 값 중 하나 이외의 값
    #DISCUSSION : 대화  또는 토론에 참여한 여러 사람
    #PRESENTATION : 하나 또는 그 이상의 사람들이 강의
    interactionTypes = [(1, speech.enums.RecognitionMetadata.InteractionType.INTERACTION_TYPE_UNSPECIFIED),
                        (2, speech.enums.RecognitionMetadata.InteractionType.DISCUSSION),
                        (3, speech.enums.RecognitionMetadata.InteractionType.PRESENTATION)]
    # 오디오 산업 카테고리
    #522291 : 소비자 금융 회사 (즉, 무담보 현금 대출)
    #522220 : 자동차 금융리스 기업
    industryNaicsCodeOfAudios = [(1, 522291),
                                 (2, 522220)]

    # 스피커에서 마이크 까지의 거리
    #MICROPHONE_DISTANCE_UNSPECIFIED : 오디오 유형을 알 수 없습니다.
    #NEARFIELD : 오디오는 밀접하게 배치 된 마이크에서 캡처했습니다 (전화, 마이크) 1미터이내
    #MIDFIELD : 스피커가 마이크에서 3 미터 이내
    microphoneDistances = [(1, speech.enums.RecognitionMetadata.MicrophoneDistance.MICROPHONE_DISTANCE_UNSPECIFIED),
                           (2, speech.enums.RecognitionMetadata.MicrophoneDistance.NEARFIELD),
                           (3, speech.enums.RecognitionMetadata.MicrophoneDistance.MIDFIELD)]

    # 오디오의 원본 오디오 또는 비디오 중 하나
    #ORIGINAL_MEDIA_TYPE_UNSPECIFIED : 알 수없는 원본 미디어 유형입니다.
    #AUDIO : 음성 데이터는 오디오 녹음입니다.
    originalMediaTypes = [(1, speech.enums.RecognitionMetadata.OriginalMediaType.ORIGINAL_MEDIA_TYPE_UNSPECIFIED),
                          (2, speech.enums.RecognitionMetadata.OriginalMediaType.AUDIO)]

    # 오디오 캡쳐 장치 종류
    #RECORDING_DEVICE_TYPE_UNSPECIFIED : 녹음 장치를 알 수 없습니다.
    #SMARTPHONE : 음성은 스마트 폰에 녹음되었습니다.
    #PHONE_LINE : 연설은 전화선을 통해 기록되었습니다.
    recordingDeviceTypes = [(1, speech.enums.RecognitionMetadata.RecordingDeviceType.RECORDING_DEVICE_TYPE_UNSPECIFIED),
                            (2, speech.enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE),
                            (3, speech.enums.RecognitionMetadata.RecordingDeviceType.PHONE_LINE)]

    for (speech_num, file_gs_path, stream_time) in files_gs_path:
        for (interactionType_idx, interactionType) in interactionTypes:
            for (industryNaicsCodeOfAudio_idx, industryNaicsCodeOfAudio) in industryNaicsCodeOfAudios:
                for (microphoneDistance_idx, microphoneDistance) in microphoneDistances:
                    for (originalMediaType_idx, originalMediaType) in originalMediaTypes:
                        for (recordingDeviceType_idx, recordingDeviceType) in recordingDeviceTypes:
                            print(' ============ START file_gs_path :', file_gs_path,
                                  ', sample_rate_hertz : ', sample_rate_hertz,
                                  ', interactionType : ', interactionType,
                                  ', industryNaicsCodeOfAudio : ', industryNaicsCodeOfAudio,
                                  ', microphoneDistance : ', microphoneDistance,
                                  ', originalMediaType : ', originalMediaType,
                                  ', recordingDeviceType : ', recordingDeviceType,
                                  ' ===============')
                            tuple_result_msg = ()
                            result_msg = ''
                            except_msg = ''
                            confidence = 0
                            stt_status = 1
                            latency = 0
                            try:
                                start_time = time.time()
                                print('start_time : ', start_time)

                                # 2-2. 긴 오디오 파일 인식 결과 가져오기
                                tuple_result_msg = beta_snippets.transcribe_gcs_with_metadata_return(file_gs_path,             #스토리지 uri
                                                                                                    sample_rate_hertz,         #샘플비율 헤르츠
                                                                                                    interactionType,           #오디오 사용 사례
                                                                                                    industryNaicsCodeOfAudio,  #오디오 산업 카테고리
                                                                                                    microphoneDistance,        #스피커에서 마이크 까지의 거리
                                                                                                    originalMediaType,         #오디오의 원본 오디오 또는 비디오 중 하나
                                                                                                    recordingDeviceType)

                                end_time = time.time()
                                latency = end_time - start_time
                                print('end_time : ', end_time)
                                print('latency : ', latency)

                                result_msg = tuple_result_msg[0]
                                confidence = tuple_result_msg[1]
                            except:
                                stt_status = -1
                                #오류가 발생하면 except_msg 변수에 담는다.
                                except_msg = sys.exc_info()
                                print("Unexpected error:", except_msg)
                                #오류 무시
                                pass
                            finally:
                                print('result_msg : ', result_msg)
                                #2-3.빅쿼리에 결과 저장
                                try:
                                    save_result_bigquery.saveBigQuery(speech_num, '2', stt_status, except_msg, result_msg,
                                                                      sample_rate_hertz, '', False, interactionType, industryNaicsCodeOfAudio,
                                                                      microphoneDistance, originalMediaType, recordingDeviceType, 0, stream_time,
                                                                      confidence, latency)

                                except:
                                    except_msg = sys.exc_info()
                                    print("Unexpected error:", except_msg)
                                    pass

                                print(' ============ END file_gs_path :', file_gs_path,
                                      ', sample_rate_hertz : ', sample_rate_hertz,
                                      ', interactionType : ', interactionType,
                                      ', industryNaicsCodeOfAudio : ', industryNaicsCodeOfAudio,
                                      ', microphoneDistance : ', microphoneDistance,
                                      ', originalMediaType : ', originalMediaType,
                                      ', recordingDeviceType : ', recordingDeviceType,
                                      ', latency : ', latency,
                                      ' ===============')

if __name__ == '__main__':
    execute()
