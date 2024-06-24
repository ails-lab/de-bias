import os
import json


LLM_ENDPOINT = os.getenv('LLM_ENDPOINT') + 'completion'
LLM_TYPE = 'completion'
FILTER_AMBIGUOUS = True
LLM_PROMPTS_FILE = os.path.join(os.getenv('VOCABULARIES_PATH'), 'llm_prompts.json')

BASE_PAYLOAD = {
    "stream": False,
    "n_predict": 10,
    "temperature": 0,
    "stop": [
        "</s>"
    ],
    "repeat_last_n": 0,
    "repeat_penalty": 0,
    "top_k": -1,
    "top_p": 0,
    "min_p": 0,
    "tfs_z": 1,
    "typical_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "cache_prompt": True,
}
BASE_HEADERS = {
    'Content-Type': 'application/json'
}

POSITIVE_RESPONSES = {
    'en': ('yes', 'Yes')
}
NEGATIVE_RESPONSES = {
    'en': ('no', 'No')
}


with open(LLM_PROMPTS_FILE, 'r') as fp:
    LLM_PROMPTS = json.load(fp)[LLM_TYPE]

