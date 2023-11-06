import stanza


def find_matches(sentence: stanza.models.common.doc.Sentence,
                 prefixed_terms: dict[str: list[str]]
                 ) -> list[tuple[str, int, int]]:
    matches = []
    sentence_lemmas = [(word.lemma, word.id, word.start_char, word.end_char)
                       for word in sentence.words]
    print(sentence_lemmas)
    for lemma, lemma_id, start_char, end_char in sentence_lemmas:
        if lemma in prefixed_terms:
            for lemmatized_term in prefixed_terms[lemma]:
                term_len = len(lemmatized_term)
                zipped_term_text = zip(
                    lemmatized_term,
                    (word.lemma
                     for word in sentence.words[lemma_id - 1: lemma_id + term_len - 1])
                )
                if all((lemma1 == lemma2 for lemma1, lemma2 in zipped_term_text)):
                    matches.append((' '.join(lemmatized_term), start_char, end_char))
                    print('Found term {} from {} to {}'.format(
                        ' '.join(lemmatized_term), start_char, end_char))
    print(matches)
    return matches
