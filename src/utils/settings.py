from collections import OrderedDict
import pickle

import stanza

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']

startup_languages = [
    'en',
]

processed_terms_filepaths = {
    'en': './samples/english_vocab_v1_processed.pickle'
}

in_memory_models = OrderedDict({
    lang: stanza.Pipeline(lang, processors='tokenize, mwt, pos, lemma, ner',
                          package={'pos': 'combined_charlm', 'lemma': 'combined_charlm'})
    for lang in startup_languages
})

in_memory_terms = OrderedDict()

for lang in startup_languages:
    with open(processed_terms_filepaths[lang], 'rb') as fp:
        in_memory_terms[lang] = pickle.load(fp)
