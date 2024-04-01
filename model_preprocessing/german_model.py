import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'de/lemma/gsd_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['mohren'] = 'mohr'

torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'de/lemma/gsd_charlm_customized.pt'))
