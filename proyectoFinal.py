from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from scipy.io.wavfile import write


import os
import re
import sounddevice as sd
import requests as reqs

sr = 16000
"""
seconds = int(input("Cuántos segundos quieres grabar?: "))
print("Puedes comenzar a grabar tu mensaje de", seconds, "segundos")
"""
duration = 10
print("Grabando...")
myrecording = sd.rec((duration * sr), samplerate=sr, channels=2)
sd.wait()
write('audio.wav', sr, myrecording)
print("Procesando...")

authenticator = IAMAuthenticator(
    'dkxIkeVQsEB7jOJLEJEYyAJ8psDiatx5b-PT-9iXOW5U')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(os.environ.get('IBM_URL'))

frases_sos = [
    "ayuda",
    "ayuda por favor",
    "auxilio",
    "necesito ayuda",
    "hay alguién ahí",
    "me caí",
    "no me siento bien",
    "me siento mal",
    "me estoy sintiendo mal",
    "estoy lastimado",
    "estoy lastimada",
    "auxilio por favor",
    "necesito que alguien me ayude",
    "nueve uno uno",
    "llamar a emergencias"
]

with open(join(dirname(__file__), 'audio.wav'), 'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model='es-MX_BroadbandModel',
    ).get_result()

texto = speech_recognition_results['results'][0]['alternatives'][0]['transcript']
parsed_text = re.split(' ', texto)
print("El mensaje grabado fue:", texto)


def compare(words, warns) -> bool:
    for word in words:
        for warn in warns:
            if word == warn:
                return True


check = compare(parsed_text, frases_sos)

if check:
    pass

if check := compare(parsed_text, frases_sos):
    print("Notificando a contactos de emergencia")
    resp = reqs.post(
        'https://maker.ifttt.com/trigger/accidente/with/key/gJWSPp3CRk-4LrM21Yyk6-r5E3-DfczEO0yz8sUrFcQ')

else:
    print("No se ha identificado una frase de emergencia, que tenga lindo día.")
