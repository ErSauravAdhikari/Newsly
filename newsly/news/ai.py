import openai
from django.conf import settings
import json
from io import BytesIO
import translators.server as tss

import requests
from gtts import gTTS


def get_tts(text: str):
    language = 'en'
    myobj = gTTS(tld="co.in", text=text, lang=language, slow=False)
    fp = BytesIO()
    myobj.write_to_fp(fp)
    return fp


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


def get_summary(text: str):
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=text,
        temperature=0.7,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )
    return response


def translate_to_nepali(text: str):
    nepali_text = tss.bing(
        query_text=text,
        from_language='en',
        to_language='ne'
    )

    return nepali_text
