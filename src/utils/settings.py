import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')
VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']

stanza_models_kwargs = {
    'en': {
        'processors': 'tokenize, mwt, pos, lemma, ner',
        'package': 'default_accurate',
        'lemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                         'en/lemma/combined_charlm_customized.pt')
    },
    'fr': {
        'processors': 'tokenize, mwt, pos, lemma, ner',
        'package': 'default_accurate',
        'lemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                         'fr/lemma/combined_charlm_customized.pt')
    },
    'nl': {
        'processors': 'tokenize, mwt, pos, lemma, ner',
        'package': 'default_accurate',
    },
    'de': {
            'processors': 'tokenize, mwt, pos, lemma, ner',
            'package': 'default_accurate',
        },
    'it': {
        'processors': 'tokenize, mwt, pos, lemma, ner',
        'package': 'default_accurate',
    }
}

startup_languages = [
    'en',
    'fr',
    'nl'
]

processed_terms_filepaths = {
    'en': os.path.join(VOCABULARIES_PATH, 'english_vocab_v1_processed.pickle'),
    'fr': os.path.join(VOCABULARIES_PATH, 'french_vocab_v1_processed.pickle'),
    'nl': os.path.join(VOCABULARIES_PATH, 'dutch_vocab_v1_processed.pickle'),
    'de': os.path.join(VOCABULARIES_PATH, 'german_vocab_v1_processed.pickle'),
    'it': os.path.join(VOCABULARIES_PATH, 'italian_vocab_v1_processed.pickle')
}
