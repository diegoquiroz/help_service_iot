import os

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from modules import Recording

authenticator = IAMAuthenticator(os.environ.get('IBM_KEY'))
speech_to_text = SpeechToTextV1(authenticator=authenticator)

speech_to_text.set_service_url(os.environ.get('IBM_URL'))

record = Recording()
