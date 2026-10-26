import json
from copy import copy

import requests

from src.utils.llm_settings import LLM_ENDPOINT, LLM_MODEL, BASE_PAYLOAD, BASE_HEADERS


def prompt_llm(messages: list[dict], choices: list[str] = None) -> str:
    print(messages)
    payload = copy(BASE_PAYLOAD)
    payload['messages'] = messages
    if LLM_MODEL:
        payload['model'] = LLM_MODEL
    if choices is not None:
        payload['structured_outputs'] = {'choice': choices}
    response = requests.request('POST',
                                LLM_ENDPOINT,
                                headers=BASE_HEADERS,
                                data=json.dumps(payload),
                                timeout=60)
    response.raise_for_status()
    response = response.json()
    # print(response['choices'][0]['message'])
    return response['choices'][0]['message']['content'] or ''
