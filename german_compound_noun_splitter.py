import stanza
from stanza.pipeline.processor import register_processor, Processor
from stanza.models.common.doc import Word
from german_compound_splitter import comp_split


@register_processor('german_compound_noun_splitter')
class GermanCompNounSplitterProcessor(Processor):
    _requires = {'tokenize', 'pos', 'lemma'}
    _provides = {'splitter'}

    def __init__(self, device, config, pipeline):
        model_path = './german/german_utf8_linux.dic'
        self._set_up_model({'model_path': model_path}, pipeline, 'cpu')

    def _set_up_model(self, config, pipeline, device):
        input_file = config['model_path']
        self._ahocs = comp_split.read_dictionary_from_file(input_file)

    def process(self, doc):
        for sent in doc.sentences:
            word_id = 1
            for token in sent.tokens:
                new_word_list = []
                for word in token.words:
                    if word.upos == 'NOUN':
                        dissection = comp_split.dissect(word.text, self._ahocs, make_singular=True)
                        if len(dissection) > 1:
                            upos = word.upos
                            xpos = word.xpos
                            feats = word.feats
                            for part in dissection:
                                new_word_dict = {
                                    'id': word_id,
                                    'text': part,
                                    'lemma': part,
                                    'upos': upos,
                                    'xpos': xpos,
                                    'feats': feats
                                }
                                word_id += 1
                                new_word = Word(sent, new_word_dict)
                                new_word_list.append(new_word)
                        else:
                            word.id = word_id
                            word_id += 1
                            new_word_list.append(word)
                    else:
                        word.id = word_id
                        word_id += 1
                        new_word_list.append(word)
                token.words = new_word_list
                token.id = tuple(word.id for word in new_word_list)
        return doc

