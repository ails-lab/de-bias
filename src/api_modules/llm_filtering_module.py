import stanza

from src.utils.api_helper_classes import Match
from src.utils.llm_settings import FILTER_AMBIGUOUS, LLM_PROMPTS, POSITIVE_RESPONSES, NEGATIVE_RESPONSES
from src.utils.prompt_llm import prompt_llm


def llm_filtering(doc: str,
                  matches: list[Match],
                  context: dict,
                  language: str = 'en'):

    filtered_matches = []

    for match in matches:
        prompt = LLM_PROMPTS[language]
        prompt = prompt.format(term=match.text,
                               context=context[match.term_uri]['context'],
                               positive_response=POSITIVE_RESPONSES[language][0],
                               negative_response=NEGATIVE_RESPONSES[language][0],
                               text=doc)
        print(prompt)
        response = prompt_llm(prompt)
        if response.startswith(POSITIVE_RESPONSES[language]):
            filtered_matches.append(match)
        elif response.startswith(NEGATIVE_RESPONSES[language]):
            print('Term {} was rejected by LLM'.format(match.text))
            continue
        else:
            print('LLM gave ambiguous response "{}" for term {}'.format(response, match.text))
            if not FILTER_AMBIGUOUS:
                filtered_matches.append(match)
        # convert to yes or no
    return filtered_matches
