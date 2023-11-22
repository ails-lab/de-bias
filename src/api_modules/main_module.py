import pickle

import stanza

from src.api_modules.filtering_module import filter_matches
from src.api_modules.matching_module import find_matches
from src.utils.settings import in_memory_models, in_memory_terms, processed_terms_filepaths


def find_terms(docs: list[str], language: str = 'en') -> list:
    if language in in_memory_models:
        nlp = in_memory_models[language]
        in_memory_models.move_to_end(language)
    else:
        nlp = stanza.Pipeline(language, processors='tokenize, lemma, ner')
        in_memory_models.popitem(last=False)
        in_memory_models[language] = nlp

    if language in in_memory_terms:
        terms = in_memory_terms[language]
        in_memory_terms.move_to_end(language)
    else:
        with open(processed_terms_filepaths[language], 'rb') as fp:
            terms = pickle.load(fp)
        in_memory_terms.popitem(last=False)
        in_memory_terms[language] = terms

    in_docs = [stanza.Document([], text=d) for d in docs]
    out_docs = nlp(in_docs)
    filtered_matches = []

    for doc in out_docs:
        for sentence in doc.sentences:
            matches = find_matches(sentence, terms)
            filtered_matches.extend(filter_matches(sentence, matches))

    return [{
        'body': match[0],
        'target': {
            'language': language,
            'literal': match[0],
            'position': {
                'start': match[1],
                'end': match[2]
            }
        }
    } for match in filtered_matches]
