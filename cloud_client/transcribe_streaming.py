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
"""Google Cloud Speech API sample application using the streaming API.
Example usage:
    python transcribe_streaming.py resources/audio.raw
"""
#스트리밍 입력에서 오디오 파일 인식
#실행 시 parameters 입력 : C:/Users/웰컴저축은행/workspace/google_stt_lab\resources\샘플1_1분.wav
#원격지에서는 google storage 경로 입력
import argparse
import io


# [START speech_transcribe_streaming]
#스트리밍 음성인식
def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    client = speech.SpeechClient()

    # [START speech_python_migration_streaming_request]
    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    print('content : ', content)
    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,  # default : 16000
        language_code='ko-KR'  # 한국어 : ko-KR
    )
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    # [START speech_python_migration_streaming_response]
    responses = client.streaming_recognize(streaming_config, requests)
    # [END speech_python_migration_streaming_request]
    print('responses : ', responses)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))
    # [END speech_python_migration_streaming_response]
# [END speech_transcribe_streaming]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    args = parser.parse_args()
    transcribe_streaming(args.stream)