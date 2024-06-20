import os
import json
from copy import copy

import requests

from src.utils.llm_settings import LLM_ENDPOINT, BASE_PAYLOAD, BASE_HEADERS


def prompt_llm(prompt):
    payload = copy(BASE_PAYLOAD)
    payload['prompt'] = prompt
    response = requests.request('POST',
                                LLM_ENDPOINT,
                                headers=BASE_HEADERS,
                                data=json.dumps(payload))
    print(response.text)
    response = response.json()
    return response['content']
