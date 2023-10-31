from itertools import groupby

import stanza

ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'PER', 'ORG', 'LOC', 'FAC', 'GPE', 'PRODUCT',
                'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']


def simple_pipeline(docs: list[str], terms: list[str]):
    nlp = stanza.Pipeline('en', processors='tokenize, lemma, ner')
    in_docs = [stanza.Document([], text=d) for d in docs]
    out_docs = nlp(in_docs)

    in_terms = [stanza.Document([], text=t) for t in terms]
    out_terms = nlp(in_terms)
    lemmatized_terms = [[word.lemma
                         for sent in doc.sentences for word in sent.words]
                        for doc in out_terms]
    sorted_terms = sorted(lemmatized_terms, key=lambda x: x[0])
    grouped_terms = groupby(sorted_terms, key=lambda x: x[0])
    prefixed_terms = {prefix: list(term_lemmas) for prefix, term_lemmas in grouped_terms}

    for doc in out_docs:
        entities = [(ent.text, ent.start_char, ent.end_char, ent.type)
                    for ent in doc.ents if ent.type in ENTITY_TYPES]
        print(entities)
        for sentence in doc.sentences:
            print(sentence.text)
            lemmas = [(word.lemma, word.id, word.start_char, word.end_char)
                      for word in sentence.words]
            for lemma, lemma_id, start_char, end_char in lemmas:
                if lemma in prefixed_terms:
                    for lemmatized_term in prefixed_terms[lemma]:
                        term_len = len(lemmatized_term)
                        zipped_term_text = zip(
                            lemmatized_term,
                            (word.lemma
                             for word in sentence.words[lemma_id - 1: lemma_id + term_len - 1])
                        )
                        if all((lemma1 == lemma2 for lemma1, lemma2 in zipped_term_text)):
                            print('Found term {} from {} to {}'.format(
                                ' '.join(lemmatized_term), start_char, end_char))
                            for ent in doc.ents:
                                if (ent.start_char <= start_char < ent.end_char
                                        or start_char <= ent.start_char < end_char):
                                    print('But term is part of entity {}'.format(ent.text))


if __name__ == '__main__':
    docs = ['This is a sentence about Winston Churchill.', 'A second sentence is here.',
            'Three sentences!']
    terms = ['be', 'bee', 'sentence', 'Churchill']
    terms = dict.fromkeys(terms)
    simple_pipeline(docs, terms)
