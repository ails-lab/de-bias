import pickle
from collections import OrderedDict
import uuid

from src.api_helper_classes import RequestMode
import stanza

from src.api_modules.filtering_module import filter_matches
from src.api_modules.matching_module import find_matches
from src.utils.settings import stanza_models_kwargs, startup_languages, processed_terms_filepaths
# need to import in order to log these as stanza processors
# ORDER MATTERS for some godforsaken reason
from src.custom_processors import german_compound_noun_splitter, standardize, delayed_lemmatizer

in_memory_models = OrderedDict({
    lang: stanza.Pipeline(lang, download_method=None, **stanza_models_kwargs[lang])
    for lang in startup_languages
})

in_memory_terms = OrderedDict()

for lang in startup_languages:
    with open(processed_terms_filepaths[lang], 'rb') as fp:
        in_memory_terms[lang] = pickle.load(fp)


def find_terms(items, language: str = 'en', mode: RequestMode = RequestMode.SIMPLE) -> list:
    
    # Load model in memory
    if language in in_memory_models:
        nlp = in_memory_models[language]
        in_memory_models.move_to_end(language)
    else:
        nlp = stanza.Pipeline(language, download_method=None, **stanza_models_kwargs[language])
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

    docs = items if mode == RequestMode.SIMPLE else items.keys()
    in_docs = [stanza.Document([], text=d) for d in docs]
    out_docs = nlp(in_docs)
    filtered_matches = []

    # TODO: need to keep reference of original value somehow
    for doc in out_docs:
        for sentence in doc.sentences:
            matches = find_matches(sentence, terms)
            filtered_matches.extend(filter_matches(sentence, matches))

    results_list = []
    
    if mode == RequestMode.SIMPLE:
        results_list = [{
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
    else:
        # TODO finalize this part
        results_list = []

        for match in filtered_matches:
            result = {
                'id': str(uuid.uuid4()),
                'type': 'Annotation',
                'motivation': 'highlighting',
                'body': match[0],
            }
            # TODO
            target = DetailedResponseItemTarget()
            result['target'] = target

            results_list.append(result)

    
    return results_list
    
