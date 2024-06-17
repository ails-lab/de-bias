import argparse
import pickle
from itertools import groupby
from typing import Optional

import stanza
import pandas as pd

from src.utils.settings import stanza_models_kwargs
from src.custom_processors import german_compound_noun_splitter, standardize, delayed_lemmatizer


def preprocess_terms(terms_filepath: str, savepath: str, language: str = 'en', ret: bool = False)\
        -> Optional[dict]:
    df = pd.read_csv(terms_filepath, dtype={'disambiguation': bool})
    terms = df['term']
    in_terms = [stanza.Document([], text=t.strip()) for t in terms]
    nlp = stanza.Pipeline(language, download_method=None, **stanza_models_kwargs[language])
    out_terms = [nlp(d) for d in in_terms]
    for i, term in enumerate(out_terms):
        if term is None:
            print(i)
            print(in_terms[i].text)
    # print([[(word.text, word.lemma)
    #         for sent in doc.sentences for word in sent.words]
    #        for doc in out_terms])
    lemmatized_terms = ([word.lemma
                         for sent in doc.sentences for word in sent.words] + [uri]
                        for doc, uri in zip(out_terms, df['uri']))
    sorted_terms = sorted(lemmatized_terms, key=lambda x: x[0])
    grouped_terms = groupby(sorted_terms, key=lambda x: x[0])
    prefixed_terms = {prefix: list(term_lemmas) for prefix, term_lemmas in grouped_terms}
    term_context = {row['uri']: row for row in df.to_dict(orient='records')}
    with open(savepath, 'wb') as fp:
        pickle.dump({'processed_terms': prefixed_terms,
                     'term_context': term_context},
                    fp)
    if ret:
        return prefixed_terms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--terms-filepath',
        type=str
    )
    parser.add_argument(
        '--savepath',
        type=str
    )
    parser.add_argument(
        '--language',
        type=str,
        choices=['en', 'de', 'fr', 'it', 'nl']
    )
    args = parser.parse_args()

    terms = preprocess_terms(args.terms_filepath, args.savepath, language=args.language, ret=True)
    print(terms)


if __name__ == '__main__':
    main()
