import os
import re
import threading
import queue
import json
import requests

from dotenv import load_dotenv
from help_words import help_words
from os.path import dirname, join
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from modules import Recording

audioqueue = queue.Queue()
load_dotenv()


def main():
    authenticator = IAMAuthenticator(os.environ.get('IBM_KEY'))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)

    speech_to_text.set_service_url(os.environ.get('IBM_URL'))

    def callback1():
        while True:
            record = Recording(duration=5)
            # Record and return buffer name
            file = record.record_audio()
            # Save buffer on a queue
            audioqueue.put(file)

    def callback2():
        while True:
            file = audioqueue.get()
            file_path = join(dirname(__file__), file)
            with open(file_path, 'rb') as audio_file:
                speech_recognition_results = speech_to_text.recognize(
                    audio=audio_file,
                    content_type='audio/wav',
                    model='es-MX_BroadbandModel',
                ).get_result()

            # Remove buffer from directory
            os.remove(file_path)

            print(json.dumps(speech_recognition_results, indent=1))
            results = speech_recognition_results['results']
            if results != []:
                text = results[0]['alternatives'][0]['transcript']
            else:
                continue
            parsed_text = re.split(' ', text)
            print("El mensaje grabado fue:", text)

            def compare(words, warns) -> bool:
                for word in words:
                    for warn in warns:
                        if word == warn:
                            return True

            if compare(parsed_text, help_words):
                print("Notificando a contactos de emergencia")
                requests.post(os.environ.get('IFTTT_URL'))

    thread1 = threading.Thread(target=callback1)
    thread1.start()
    thread2 = threading.Thread(target=callback2)
    thread2.start()
    while True:
        pass


if __name__ == "__main__":
    main()
