import itertools

import stanza
from stanza.pipeline.processor import register_processor, Processor
from stanza.models.common.doc import Word


@register_processor('standardize')
class GermanCompNounSplitterProcessor(Processor):
    _requires = {'tokenize', 'pos', 'ner'}
    _provides = {'standardize'}

    def __init__(self, device, config, pipeline):
        pass

    def _set_up_model(self, config, pipeline, device):
        pass

    def process(self, doc):
        for sent in doc.sentences:
            for token in sent.tokens:
                for word in token.words:
                    word._start_char = token.start_char
                    word._end_char = token.end_char
                    word.text = word.text.lower()
        return doc

