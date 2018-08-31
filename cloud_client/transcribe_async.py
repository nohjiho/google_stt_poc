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
#gs://dlab_ml/speech/ref/샘플1_1분.wav
import argparse
import io


# [START speech_transcribe_async]
def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_async_request]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,  # default : 16000
        language_code='ko-KR'  # 한국어 : ko-KR
    )

    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END speech_python_migration_async_request]

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
    # [END speech_python_migration_async_response]
# [END speech_transcribe_async]

# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,  # default : 16000
        language_code='ko-KR'  # 한국어 : ko-KR
    )

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
# [END speech_transcribe_async_gcs]

# [START transcribe_gcs_return]
def transcribe_gcs_return(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,  # default : 16000
        language_code='ko-KR'  # 한국어 : ko-KR
    )

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    tuple_result_msg = ()
    result_msg = ''
    confidence = 0
    print('len : ', len(response.results))
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))

        result_msg += result.alternatives[0].transcript + ' '
        confidence += result.alternatives[0].confidence


    #결과를 빅쿼리에 저장하기 위해 return
    tuple_result_msg = (result_msg, confidence/len(response.results))
    return tuple_result_msg
# [END transcribe_gcs_return]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
        #transcribe_gcs_return(gcs_uri)
    else:
        transcribe_file(args.path)