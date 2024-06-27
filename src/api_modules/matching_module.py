from itertools import zip_longest

import stanza


def find_matches(sentence: stanza.models.common.doc.Sentence,
                 prefixed_terms: dict[str: list[str]]
                 ) -> list[tuple[str, int, int, int]]:
    matches = []
    # print(sentence.words)
    # print(sentence.tokens)
    for word in sentence.words:
        if word.lemma not in prefixed_terms:
            continue
        for lemmatized_term in prefixed_terms[word.lemma]:
            term_len = len(lemmatized_term)
            zipped_term_text = zip_longest(
                lemmatized_term[:-1],  # last element is term uri
                sentence.words[word.id - 1: word.id + term_len - 2]
            )
            if any((sentence_word is None or term_lemma != sentence_word.lemma
                    for term_lemma, sentence_word in zipped_term_text)):
                continue
            matches.append(
                (
                    lemmatized_term[-1],
                    word.start_char,
                    sentence.words[word.id + term_len - 3].end_char,
                    word.id
                )
            )
    # print('unfiltered matches', matches)
    return matches
