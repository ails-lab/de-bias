from collections import OrderedDict
import pickle
import os

import stanza

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']

stanza_models_kwargs = {
    'en': {
        'processors': 'tokenize, mwt, pos, lemma, ner',
        'package': {'pos': 'combined_charlm', 'lemma': 'combined_charlm'},
        'lemma_model_path': os.path.join(os.getenv('STANZA_PATH'),
                                         'en/lemma/combined_charlm_customized.pt')
    }
}

startup_languages = [
    'en',
]

processed_terms_filepaths = {
    'en': './samples/english_vocab_v1_processed.pickle'
}

in_memory_models = OrderedDict({
    lang: stanza.Pipeline(lang, **stanza_models_kwargs[lang])
    for lang in startup_languages
})

in_memory_terms = OrderedDict()

for lang in startup_languages:
    with open(processed_terms_filepaths[lang], 'rb') as fp:
        in_memory_terms[lang] = pickle.load(fp)
