import stanza
from stanza.pipeline.processor import register_processor
from stanza.pipeline.lemma_processor import LemmaProcessor
from stanza.pipeline._constants import LEMMA, TOKENIZE, MWT, NER, POS


@register_processor('delayedlemma')
class DelayedLemmaProcessor(LemmaProcessor):
    _requires = {'tokenize', 'pos', 'ner', 'standardize'}
    _provides = {'lemma'}
    PROVIDES_DEFAULT = {LEMMA}
    REQUIRES_DEFAULT = {TOKENIZE, MWT, NER, 'standardize'}

    def __init__(self, config, pipeline, device):
        # print(config)
        super().__init__(config, pipeline, device)

    def _set_up_requires(self):
        self._pretagged = self._config.get('pretagged', None)
        if self._pretagged:
            self._requires = set()
        elif self.config.get('pos') and not self.use_identity:
            self._requires = DelayedLemmaProcessor.REQUIRES_DEFAULT.union({POS})
        else:
            self._requires = DelayedLemmaProcessor.REQUIRES_DEFAULT

    def process(self, document):
        document = super().process(document)
        for sent in document.sentences:
            for word in sent.words:
                if word.lemma is None:
                    word.lemma = word.text.lower()
        if self._pipeline.lang == 'de':
            for sent in document.sentences:
                for word in sent.words:
                    word.lemma = word.lemma.lower()
        return document
