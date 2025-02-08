import json
from copy import copy

import requests

from src.utils.llm_settings import LLM_ENDPOINT, BASE_PAYLOAD, BASE_HEADERS


def prompt_llm(prompt: str) -> str:
    # print(prompt)
    payload = copy(BASE_PAYLOAD)
    payload['prompt'] = prompt
    response = requests.request('POST',
                                LLM_ENDPOINT,
                                headers=BASE_HEADERS,
                                data=json.dumps(payload),
                                timeout=5)
    response = response.json()
    # print(response['content'])
    return response['content']
