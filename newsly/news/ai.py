from django.conf import settings
import json
from io import BytesIO

import requests
from gtts import gTTS


def get_tts(text: str):
    language = 'en'
    myobj = gTTS(tld="co.in", text=text, lang=language, slow=False)
    fp = BytesIO()
    myobj.write_to_fp(fp)
    return fp

    # Playing the converted file
    # os.system("mpg321 welcome.mp3")


def get_tts_ibm(text: str):
    url = settings.IBM_WATSON_TTS_URL

    data = json.dumps({
        "text": text
    })
    res = requests.post(
        f"{url}/v1/synthesize?voice=en-US_MichaelExpressive",
        headers={
            "Content-Type": "application/json",
            "Accept": "audio/wav",
            'Authorization': settings.IBM_WATSON_TTS_AUTHORIZATION,
        },
        data=data
    )
    return res.content
