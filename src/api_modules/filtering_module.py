import stanza

from src.utils.settings import ENTITY_TYPES


def filter_matches(sentence: stanza.models.common.doc.Sentence,
                   matches: list[tuple[str, int, int]]
                   ) -> list[tuple[str, int, int]]:
    filtered_matches = []

    entities = [(ent.text, ent.start_char, ent.end_char, ent.type)
                for ent in sentence.ents if ent.type in ENTITY_TYPES]

    print('entities', entities)

    for match in matches:
        lemmatized_term, term_start_char, term_end_char = match
        for ent_text, ent_start_char, ent_end_char, ent_type in entities:
            if ent_start_char <= term_start_char and term_end_char <= ent_end_char:
                print('Term {} is part of entity {}'.format(lemmatized_term, ent_text))
                break
        else:
            filtered_matches.append(match)
    print('filtered matches', filtered_matches)
    return filtered_matches
