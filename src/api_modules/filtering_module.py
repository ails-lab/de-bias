import stanza

from src.utils.api_helper_classes import Match
from src.utils.settings import ENTITY_TYPES


def filter_matches(sentence: stanza.models.common.doc.Sentence,
                   matches: list[Match]
                   ) -> list[Match]:
    filtered_matches = []

    entities = [(ent.text, ent.start_char, ent.end_char, ent.type)
                for ent in sentence.ents if ent.type in ENTITY_TYPES]

    # print('entities', entities)

    for match in matches:
        for ent_text, ent_start_char, ent_end_char, ent_type in entities:
            if ent_start_char <= match.start_char and match.end_char <= ent_end_char:
                print('Term {} is part of entity {}'.format(match.term, ent_text))
                break
        else:
            filtered_matches.append(match)
    # print('filtered matches', filtered_matches)
    return filtered_matches
