import json
from copy import copy

import requests

from src.utils.llm_settings import LLM_ENDPOINT, BASE_PAYLOAD, BASE_HEADERS


def prompt_llm(prompt: str, grammar: str = None) -> str:
    print(prompt)
    payload = copy(BASE_PAYLOAD)
    payload['prompt'] = prompt
    if grammar is not None:
        payload['grammar'] = grammar
    response = requests.request('POST',
                                LLM_ENDPOINT,
                                headers=BASE_HEADERS,
                                data=json.dumps(payload),
                                timeout=60)
    response = response.json()
    # print(response['content'])
    return response['content']
