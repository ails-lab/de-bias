from itertools import zip_longest

import Levenshtein
import stanza

from src.utils.api_helper_classes import Match


def find_matches(sentence: stanza.models.common.doc.Sentence,
                 prefixed_terms: dict[str: list[str]]
                 ) -> list[Match]:
    matches = []
    # print(sentence.words)
    # print(sentence.tokens)
    for word in sentence.words:
        if word.lemma not in prefixed_terms:
            continue
        # we only keep the longest match
        # that is most similar to original text
        best_match = None
        best_match_length = 0
        best_match_distance = 0
        for lemmatized_term in prefixed_terms[word.lemma]:
            term_len = len(lemmatized_term)
            # we need zip_longest because the sentence might have
            # fewer words than the term
            zipped_term_text = zip_longest(
                lemmatized_term[:-1],  # last element is term (literal, uri)
                sentence.words[word.id - 1: word.id + term_len - 2]
            )
            # if sentence_word is None then the sentence has
            # fewer words than the term
            if any((sentence_word is None or term_lemma != sentence_word.lemma
                    for term_lemma, sentence_word in zipped_term_text)):
                continue
            start_char = word.start_char
            end_char = sentence.words[word.id + term_len - 3].end_char
            match_length = end_char - start_char
            # check if there's a longer match
            if best_match_length > match_length:
                continue
            match_text = sentence.text[start_char:end_char]
            match_distance = Levenshtein.distance(match_text, lemmatized_term[-1][0],
                                                  weights=(2, 2, 3))
            match = Match(
                term_uri=lemmatized_term[-1][1],  # term uri
                term_literal=lemmatized_term[-1][0],  # term literal
                issue_description=None,
                text=match_text,
                start_char=start_char,
                end_char=end_char,
                sentence_index=None,
                word_id=word.id
            )
            # we keep this match if it's the first
            # or if it's the longest
            # or if it's the same length but most similar
            if (
                    best_match is None
                    or best_match_length < match_length
                    or best_match_distance > match_distance
            ):
                best_match = match
                best_match_length = match_length
                best_match_distance = match_distance
        # no matches found
        if best_match is None:
            continue
        # we need to check if this new match is contained in the previous one
        # if this is the first match found we are ok
        if not matches:
            matches.append(best_match)
            continue
        # we know this match starts after the previous one
        # but if it also ends before it then it is contained
        if matches[-1].end_char < best_match.end_char:
            matches.append(best_match)
    # print('unfiltered matches', matches)
    return matches
