#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#로컬 파일에서 동기 음성 인식 수행
# [START speech_quickstart]
import io
import os

# Imports the Google Cloud client library
# [START migration_import]
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# [END migration_import]

def run_quickstart():
    # Instantiates a client
    # [START migration_client]
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        '샘플1_1분.wav')

    print('file_name : ', file_name)
    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000, # default : 16000
        language_code='ko-KR' # 한국어 : ko-KR
    )

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    print('response : ', response)
    print('response.results : ', response.results)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]

if __name__ == '__main__':
    print('name : ', __name__)
    run_quickstart()
