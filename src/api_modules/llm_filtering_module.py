import json

import stanza

from src.utils.api_helper_classes import Match
from src.utils.llm_settings import FILTER_AMBIGUOUS, POSITIVE_RESPONSES, \
    NEGATIVE_RESPONSES, LLM_PROMPTS_FILE
from src.utils import llm_settings
from src.utils.prompt_llm import prompt_llm


def llm_filtering(texts: list[str],
                  matches: list[Match],
                  context: dict,
                  language: str = 'en',
                  reload_prompts: bool = False) -> list[Match]:
    filtered_matches = []
    if reload_prompts:
        with open(LLM_PROMPTS_FILE, 'r') as fp:
            llm_settings.LLM_PROMPTS = json.load(fp)
    for text, match in zip(texts, matches):
        if not context[(match.term_literal, match.term_uri)]['disambiguation']:
            filtered_matches.append(match)
            continue
        prompt = llm_settings.LLM_PROMPTS[language]
        prompt = prompt.format(term=match.term_literal,
                               context=context[(match.term_literal, match.term_uri)]['context'],
                               positive_response=POSITIVE_RESPONSES[language][0],
                               negative_response=NEGATIVE_RESPONSES[language][0],
                               text=text)
        # print(prompt)
        grammar = 'root::=("{}" | "{}").*'.format(POSITIVE_RESPONSES[language][1],
                                                  NEGATIVE_RESPONSES[language][1])
        response = prompt_llm(prompt, grammar).strip()
        if response.startswith(POSITIVE_RESPONSES[language]):
            filtered_matches.append(match)
        elif response.startswith(NEGATIVE_RESPONSES[language]):
            # print('Term {} was rejected by LLM'.format(match.text))
            continue
        else:
            # print('LLM gave ambiguous response "{}" for term {}'.format(response, match.text))
            if not FILTER_AMBIGUOUS:
                filtered_matches.append(match)
        # convert to yes or no
    return filtered_matches
