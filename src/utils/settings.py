import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')
VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']

stanza_models_kwargs = {
    'en': {
        'processors': 'tokenize, mwt, pos, lemma, ner',
        'package': {'pos': 'combined_charlm', 'lemma': 'combined_charlm'},
        'lemma_model_path': os.path.join(STANZA_RESOURCES_DIR,
                                         'en/lemma/combined_charlm_customized.pt')
    }
}

startup_languages = [
    'en',
]

processed_terms_filepaths = {
    'en': os.path.join(VOCABULARIES_PATH, 'english_vocab_v1_processed.pickle')
}
