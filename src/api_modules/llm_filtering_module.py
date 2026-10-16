import stanza

from src.utils.api_helper_classes import Match
from src.utils.llm_settings import FILTER_AMBIGUOUS, POSITIVE_RESPONSES, \
    NEGATIVE_RESPONSES
from src.utils import llm_settings
from src.utils.prompt_llm import prompt_llm


def llm_filtering(texts: list[str],
                  matches: list[Match],
                  context: dict,
                  language: str = 'en',
                  reload_prompts: bool = False) -> list[Match]:
    filtered_matches = []
    if reload_prompts:
        llm_settings.LLM_PROMPTS = llm_settings.load_prompts()
    for text, match in zip(texts, matches):
        if not context[(match.term_literal, match.term_uri)]['disambiguation']:
            filtered_matches.append(match)
            continue
        fields = dict(term=match.term_literal,
                      context=context[(match.term_literal, match.term_uri)]['context'],
                      positive_response=POSITIVE_RESPONSES[language][0],
                      negative_response=NEGATIVE_RESPONSES[language][0],
                      text=text)
        messages = [{'role': message['role'], 'content': message['content'].format(**fields)}
                    for message in llm_settings.LLM_PROMPTS[language]]
        choices = [POSITIVE_RESPONSES[language][1], NEGATIVE_RESPONSES[language][1]]
        response = prompt_llm(messages, choices).strip()
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
