import pickle
from collections import OrderedDict

from src.api_modules.llm_filtering_module import llm_filtering
from src.utils.api_helper_classes import RequestMode, Match, AnnotationMatch
import stanza
import urllib.parse
from src.api_modules.ner_filtering_module import ner_filtering
from src.api_modules.matching_module import find_matches
from src.utils.settings import STANZA_MODELS_KWARGS, STARTUP_LANGUAGES, PROCESSED_TERMS_FILEPATHS
# need to import in order to log these as stanza processors
# ORDER MATTERS for some godforsaken reason
from src.custom_processors import german_compound_noun_splitter, standardize, delayed_lemmatizer


in_memory_models = OrderedDict({
    lang: stanza.Pipeline(lang, **STANZA_MODELS_KWARGS[lang])
    for lang in STARTUP_LANGUAGES
})

in_memory_terms = OrderedDict()

for lang in STARTUP_LANGUAGES:
    with open(PROCESSED_TERMS_FILEPATHS[lang], 'rb') as fp:
        in_memory_terms[lang] = pickle.load(fp)


def find_terms(docs, language: str = 'en', mode: RequestMode = RequestMode.SIMPLE,
               use_ner: bool = True, use_llm: bool = False):
    # Load model in memory
    if language in in_memory_models:
        nlp = in_memory_models[language]
        in_memory_models.move_to_end(language)
    elif language == 'corporate':
        nlp = stanza.Pipeline('en', **STANZA_MODELS_KWARGS[language])
        in_memory_models.popitem(last=False)
        in_memory_models[language] = nlp
    else:
        nlp = stanza.Pipeline(language, **STANZA_MODELS_KWARGS[language])
        in_memory_models.popitem(last=False)
        in_memory_models[language] = nlp

    if language in in_memory_terms:
        terms = in_memory_terms[language]['processed_terms']
        term_context = in_memory_terms[language]['term_context']
        in_memory_terms.move_to_end(language)
    else:
        with open(PROCESSED_TERMS_FILEPATHS[language], 'rb') as fp:
            terms = pickle.load(fp)
        in_memory_terms.popitem(last=False)
        in_memory_terms[language] = terms
        term_context = terms['term_context']
        terms = terms['processed_terms']

    in_docs = [stanza.Document([], text=d) for d in docs]
    out_docs = nlp(in_docs)
    # print('tokens')
    # for doc in out_docs:
    #     print(doc)
    #     for sentence in doc.sentences:
    #         for token in sentence.words:
    #             print(token.text, end=' ')
    #     print()
    # print(out_docs)
    filtered_matches_by_doc = []

    # TODO: need to keep reference of original value somehow
    for doc in out_docs:
        filtered_matches = []
        for sentence_id, sentence in enumerate(doc.sentences):
            matches = [Match(match[0], doc.text[match[1]:match[2]], match[1], match[2],
                             sentence_id, match[3])
                       for match in find_matches(sentence, terms)]
            if use_ner:
                matches = ner_filtering(sentence, matches)
            if use_llm and language != 'nl':  # LLM filtering switched off for Dutch
                matches = llm_filtering(doc.text, matches, term_context, language)
            filtered_matches.extend(matches)
        filtered_matches_by_doc.append(filtered_matches)
    
    if mode == RequestMode.SIMPLE:
        results = []
        for doc, matches in zip(docs,filtered_matches_by_doc):
            tags = []
            for match in matches:
                tags.append({
                    'uri': match.term_uri,
                    'start': match.start_char,
                    'end': match.end_char,
                    'length': match.end_char - match.start_char
                })
            result = {
                'language': language,
                'literal': doc,
                'tags': tags
            }
            results.append(result)
        return results
    elif mode == RequestMode.DETAILED:
        results_list = []
        for matches, doc in zip(filtered_matches_by_doc, out_docs):
            matches_with_prefix_suffix = []
            for match in matches:
                # find prefix
                # print(doc.text)
                # print(match)
                start_char = match.start_char
                if start_char - 50 <= 0:
                    prefix = doc.text[:start_char]
                else:
                    left_char_index = start_char
                    left_word_index = match.word_id - 1  # word ids start at 1
                    left_sentence_index = match.sentence_index
                    while left_char_index > start_char - 50:
                        if left_word_index > 0:
                            left_word_index -= 1
                            left_char_index = (doc.sentences[left_sentence_index]
                                               .words[left_word_index].start_char)
                        elif left_sentence_index > 0:
                            left_sentence_index -= 1
                            left_word_index = len(doc.sentences[left_sentence_index].words) - 1
                            left_char_index = (doc.sentences[left_sentence_index]
                                               .words[left_word_index].start_char)
                        else:
                            left_char_index = 0
                            break
                    prefix = doc.text[left_char_index:start_char]
                # find suffix
                end_char = match.end_char
                if end_char + 50 >= len(doc.text) - 1:
                    suffix = doc.text[end_char:]
                else:
                    right_char_index = end_char
                    right_word_index = match.word_id - 1  # word ids start at 1
                    right_sentence_index = match.sentence_index
                    right_word_last_index = len(doc.sentences[right_sentence_index].words) - 1
                    right_sentence_last_index = len(doc.sentences) - 1
                    while right_char_index < end_char + 50:
                        if right_word_index < right_word_last_index:
                            right_word_index += 1
                            right_char_index = (doc.sentences[right_sentence_index]
                                                .words[right_word_index].end_char)
                        elif right_sentence_index < right_sentence_last_index:
                            right_sentence_index += 1
                            right_word_index = 0
                            right_word_last_index = len(doc.sentences[right_sentence_index].words) - 1
                            right_char_index = (doc.sentences[right_sentence_index]
                                                .words[0].end_char)
                        else:
                            right_char_index = None
                            break
                    suffix = doc.text[end_char:right_char_index]
                matches_with_prefix_suffix.append(AnnotationMatch(match.term_uri, match.text,
                                                                  prefix, suffix))
            results_list.append(matches_with_prefix_suffix)
        return results_list
    else:
        raise ValueError('Unexpected request mode')
    
