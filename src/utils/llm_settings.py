import os
import json


LLM_ENDPOINT = os.getenv('LLM_ENDPOINT').rstrip('/') + '/v1/chat/completions'
# Optional: vLLM falls back to the model it serves when a request names none
LLM_MODEL = os.getenv('LLM_MODEL')
FILTER_AMBIGUOUS = True
LLM_PROMPTS_FILE = os.path.join(os.getenv('VOCABULARIES_PATH'), 'prompts', 'llm_prompts.json')

BASE_PAYLOAD = {
    "stream": False,
    "max_tokens": 6,
    "temperature": 0,
}
BASE_HEADERS = {
    'Content-Type': 'application/json'
}

POSITIVE_RESPONSES = {
    'en': ('yes', 'Yes'),
    'fr': ('oui', 'Oui'),
    'nl': ('ja', 'Ja'),
    'it': ('sì', 'Sì'),
    'de': ('ja', 'Ja'),
}
NEGATIVE_RESPONSES = {
    'en': ('no', 'No'),
    'fr': ('non', 'Non'),
    'nl': ('nee', 'Nee', 'neen', 'Neen'),
    'it': ('no', 'No'),
    'de': ('nein', 'Nein'),
}


def load_prompts() -> dict[str, list[dict]]:
    """Each language maps to a list of chat messages ({"role": ..., "content": ...})."""
    with open(LLM_PROMPTS_FILE, 'r') as fp:
        prompts = json.load(fp)
    for language, messages in prompts.items():
        if not isinstance(messages, list):
            raise ValueError('{}: the prompt for "{}" must be a list of chat messages'
                             .format(LLM_PROMPTS_FILE, language))
    return prompts


LLM_PROMPTS = load_prompts()
