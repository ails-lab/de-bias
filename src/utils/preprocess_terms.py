import pickle
from itertools import groupby
from typing import Optional

import stanza


def preprocess_terms(terms_filepath: str, savepath: str, language: str = 'en', ret: bool = False)\
        -> Optional[dict]:
    with open(terms_filepath, 'r') as fp:
        term_lines = fp.readlines()
    in_terms = [stanza.Document([], text=t.strip()) for t in term_lines]
    nlp = stanza.Pipeline(language, processors='tokenize, lemma')
    out_terms = nlp(in_terms)
    lemmatized_terms = ([word.lemma.lower()
                         for sent in doc.sentences for word in sent.words]
                        for doc in out_terms)
    sorted_terms = sorted(lemmatized_terms, key=lambda x: x[0])
    grouped_terms = groupby(sorted_terms, key=lambda x: x[0])
    prefixed_terms = {prefix: list(term_lemmas) for prefix, term_lemmas in grouped_terms}
    with open(savepath, 'wb') as fp:
        pickle.dump(prefixed_terms, fp)
    if ret:
        return prefixed_terms
