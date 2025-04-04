import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')
VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']

STANZA_MODELS_KWARGS = {
    'en': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, ner, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'en/lemma/combined_charlm_customized.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'en/forward_charlm/1billion.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'en/backward_charlm/1billion.pt'),
        'delayedlemma_pretrain_path': os.path.join(STANZA_RESOURCES_DIR,
                                                   'en/pretrain/conll17.pt'),
    },
    'fr': {
        'download_method': 'reuse_resources',
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
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, ner, standardize, dutch_compound_noun_splitter, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'nl/lemma/alpino_charlm_customized.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'nl/forward_charlm/ccwiki.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'nl/backward_charlm/ccwiki.pt')
    },
    'de': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, ner, standardize, german_compound_noun_splitter, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'de/lemma/gsd_charlm_customized.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'de/forward_charlm/newswiki.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'de/backward_charlm/newswiki.pt')
        },
    'it': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, ner, standardize, delayedlemma',
        'package': 'default_accurate',
        'delayedlemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                                'it/lemma/combined_charlm_customized.pt'),
        'delayedlemma_forward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                         'it/forward_charlm/conll17.pt'),
        'delayedlemma_backward_charlm_path': os.path.join(STANZA_RESOURCES_DIR,
                                                          'it/backward_charlm/conll17.pt')
    },
}

STARTUP_LANGUAGES = [
    'en',
    'it',
    'de',
    'fr',
    'nl',
]

PROCESSED_TERMS_FILEPATHS = {
    'en': os.path.join(VOCABULARIES_PATH, 'en_published_vocab_processed.pickle'),
    'fr': os.path.join(VOCABULARIES_PATH, 'fr_published_vocab_processed.pickle'),
    'nl': os.path.join(VOCABULARIES_PATH, 'nl_published_vocab_processed.pickle'),
    'de': os.path.join(VOCABULARIES_PATH, 'de_published_vocab_processed.pickle'),
    'it': os.path.join(VOCABULARIES_PATH, 'it_published_vocab_processed.pickle'),
}
