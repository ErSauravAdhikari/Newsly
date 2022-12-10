from django.conf import settings
import json

import requests


def get_tts(text: str):
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
