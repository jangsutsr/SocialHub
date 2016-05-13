from requests.auth import HTTPBasicAuth
import requests
import json
import wave

tts_usersame = 'tts_usersame'
tts_password = 'tts_password'
tts_auth=HTTPBasicAuth(tts_usersame, tts_password)

tts_url = 'https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize'
tts_headers = {'Content-Type': 'application/json', 'Accept': 'audio/flac', 'Voice': 'en-US_LisaVoice'}
text = 'I need your helps.'
data = requests.post(tts_url, auth=tts_auth, headers=tts_headers, data=json.dumps({'text': text, 'voice': 'en-US_LisaVoice'}))
file = open('now.flac', 'w')
file.write(data.content)
file.close()
