import stanza

ENTITY_TYPES = ['PERSON']


def simple_pipeline(docs, terms):
    nlp = stanza.Pipeline('en', processors='tokenize, lemma, ner')
    in_docs = [stanza.Document([], text=d) for d in docs]
    out_docs = nlp(in_docs)
    for doc in out_docs:
        lemmas = [(word.lemma, word.start_char, word.end_char)
                  for sent in doc.sentences for word in sent.words]
        entities = [(ent.text, ent.start_char, ent.end_char, ent.type)
                    for ent in doc.ents if ent.type in ENTITY_TYPES]
        print(entities)
        print(doc.text)
        for lemma, start_char, end_char in lemmas:
            if lemma in terms:
                print('Found term {} from {} to {}'.format(lemma, start_char, end_char))
                for ent in doc.ents:
                    if (ent.start_char <= start_char < ent.end_char
                            or start_char <= ent.start_char < end_char):
                        print('But term is part of entity {}'.format(ent.text))


if __name__ == '__main__':
    docs = ['This is a sentence about Winston Churchill.', 'A second sentence is here.', 'Three sentences!']
    terms = ['be', 'bee', 'sentence', 'Churchill']
    terms = dict.fromkeys(terms)
    simple_pipeline(docs, terms)
