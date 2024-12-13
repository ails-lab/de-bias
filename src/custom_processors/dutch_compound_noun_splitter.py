import itertools
import os

import stanza
from stanza.pipeline.processor import register_processor, Processor
from stanza.models.common.doc import Word

from src.utils import comp_split_dutch

VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')


@register_processor('dutch_compound_noun_splitter')
class GermanCompNounSplitterProcessor(Processor):
    _requires = {'tokenize', 'pos', 'delayedlemma'}
    _provides = {'splitter'}

    def __init__(self, device, config, pipeline):
        model_path = os.path.join(VOCABULARIES_PATH, './nl-NL.dic')
        self._set_up_model({'model_path': model_path}, pipeline, 'cpu')

    def _set_up_model(self, config, pipeline, device):
        input_file = config['model_path']
        # TODO: save the ahocs in preprocessing and just load it here
        self._ahocs = comp_split_dutch.read_dictionary_from_file(input_file)

    def process(self, doc):
        for sent in doc.sentences:
            word_id = 1
            for token in sent.tokens:
                new_word_list = []
                for word in token.words:
                    if word.upos not in ['NOUN', 'PROPN']:
                        word.id = word_id
                        word_id += 1
                        new_word_list.append(word)
                    else:
                        try:
                            dissection = comp_split_dutch.dissect(
                                word.text, self._ahocs, make_singular=True)
                        except Exception as e:
                            print(e)
                            dissection = [word.text]
                        # print(dissection)
                        if len(dissection) <= 1:
                            word.text = word.text.lower()
                            word.id = word_id
                            word_id += 1
                            new_word_list.append(word)
                        else:
                            upos = word.upos
                            xpos = word.xpos
                            feats = word.feats
                            for part in dissection:
                                new_word_dict = {
                                    'id': word_id,
                                    'text': part.lower(),
                                    'lemma': part.lower(),
                                    'upos': upos,
                                    'xpos': xpos,
                                    'feats': feats,
                                    'start_char': token.start_char,
                                    'end_char': token.end_char
                                }
                                word_id += 1
                                new_word = Word(sent, new_word_dict)
                                new_word_list.append(new_word)
                token.words = new_word_list
                token.id = tuple(word.id for word in new_word_list)
            sent.words = list(itertools.chain.from_iterable(token.words for token in sent.tokens))
        doc._count_words()
        return doc

