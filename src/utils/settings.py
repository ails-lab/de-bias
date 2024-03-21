import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')
VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']

stanza_models_kwargs = {
    'en': {
        'processors': 'tokenize, mwt, pos, ner, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'en/lemma/combined_charlm_customized.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'en/forward_charlm/1billion.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'en/backward_charlm/1billion.pt')
    },
    'fr': {
        'processors': 'tokenize, mwt, pos, ner, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'fr/lemma/combined_charlm_customized.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'fr/forward_charlm/newswiki.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'fr/backward_charlm/newswiki.pt')
    },
    'nl': {
        'processors': 'tokenize, mwt, pos, ner, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'nl/lemma/alpino_charlm.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'nl/forward_charlm/ccwiki.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'nl/backward_charlm/ccwiki.pt')
    },
    'de': {
        'processors': 'tokenize, mwt, pos, ner, german_compound_noun_splitter, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'de/lemma/gsd_charlm.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'de/forward_charlm/newswiki.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'de/backward_charlm/newswiki.pt')
        },
    'it': {
        'processors': 'tokenize, mwt, pos, ner, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'it/lemma/combined_charlm.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'it/forward_charlm/conll17.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'it/backward_charlm/conll17.pt')
    }
}

startup_languages = [
    'en',
    'it',
    'de',
    'fr',
    'nl'
]

processed_terms_filepaths = {
    'en': os.path.join(VOCABULARIES_PATH, 'english_vocab_v2_processed.pickle'),
    'fr': os.path.join(VOCABULARIES_PATH, 'french_vocab_v2_processed.pickle'),
    'nl': os.path.join(VOCABULARIES_PATH, 'dutch_vocab_v2_processed.pickle'),
    'de': os.path.join(VOCABULARIES_PATH, 'german_vocab_v2_processed.pickle'),
    'it': os.path.join(VOCABULARIES_PATH, 'italian_vocab_v2_processed.pickle')
}
