import stanza


def find_matches(sentence: stanza.models.common.doc.Sentence,
                 prefixed_terms: dict[str: list[str]]
                 ) -> list[tuple[str, int, int]]:
    matches = []
    # print(sentence.words)
    print(sentence.tokens)
    for word in sentence.words:
        if word.lemma in prefixed_terms:
            for lemmatized_term in prefixed_terms[word.lemma]:
                term_len = len(lemmatized_term)
                zipped_term_text = zip(
                    lemmatized_term,
                    sentence.words[word.id - 1: word.id + term_len - 1]
                )
                if all((term_lemma == sentence_word.lemma
                        for term_lemma, sentence_word in zipped_term_text)):
                    matches.append((' '.join(lemmatized_term),
                                    word.start_char,
                                    sentence.words[word.id + term_len - 2].end_char))
    print('unfiltered matches', matches)
    return matches
