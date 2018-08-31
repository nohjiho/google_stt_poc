#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample that demonstrates enhanced models
and recognition metadata.
Example usage:
    python beta_snippets.py enhanced-model
    python beta_snippets.py metadata
    python beta_snippets.py punctuation
    python beta_snippets.py diarization
    python beta_snippets.py multi-channel
    python beta_snippets.py multi-language
    python beta_snippets.py word-level-conf
"""

import argparse
import io


def transcribe_gcs_with_metadata(gcs_uri):
    """Send a request that includes recognition metadata."""
    # [START speech_transcribe_recognition_metadata_beta]
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()
    audio = speech.types.RecognitionAudio(uri=gcs_uri)

    # Here we construct a recognition metadata object.
    # Most metadata fields are specified as enums that can be found
    # in speech.enums.RecognitionMetadata
    metadata = speech.types.RecognitionMetadata()
    metadata.interaction_type = (
        speech.enums.RecognitionMetadata.InteractionType.DISCUSSION)
    metadata.microphone_distance = (
        speech.enums.RecognitionMetadata.MicrophoneDistance.NEARFIELD)
    metadata.recording_device_type = (
        speech.enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE)
    # Some metadata fields are free form strings
    metadata.recording_device_name = "Pixel 2 XL"
    # And some are integers, for instance the 6 digit NAICS code
    # https://www.naics.com/search/
    metadata.industry_naics_code_of_audio = 519190

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='ko-KR',
        # Add this in the request to send metadata.
        metadata=metadata)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_recognition_metadata_beta]

def transcribe_file_with_metadata():
    """Send a request that includes recognition metadata."""
    # [START speech_transcribe_recognition_metadata_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'C:/Users/웰컴저축은행/workspace/google_stt_poc/resources/샘플_4_개인정보삭제.wav'

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    # Here we construct a recognition metadata object.
    # Most metadata fields are specified as enums that can be found
    # in speech.enums.RecognitionMetadata
    metadata = speech.types.RecognitionMetadata()
    metadata.interaction_type = (
        speech.enums.RecognitionMetadata.InteractionType.DISCUSSION)
    metadata.microphone_distance = (
        speech.enums.RecognitionMetadata.MicrophoneDistance.NEARFIELD)
    metadata.recording_device_type = (
        speech.enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE)
    # Some metadata fields are free form strings
    metadata.recording_device_name = "Pixel 2 XL"
    # And some are integers, for instance the 6 digit NAICS code
    # https://www.naics.com/search/
    metadata.industry_naics_code_of_audio = 519190

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='ko-KR',
        # Add this in the request to send metadata.
        metadata=metadata)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_recognition_metadata_beta]

if __name__ == '__main__':
    #transcribe_file_with_metadata()
    transcribe_gcs_with_metadata('gs://dlab_ml/speech/ref/샘플_4_개인정보삭제.wav')

