import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'de/lemma/gsd_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['mohren'] = 'mohr'
word_dict['negerin'] = word_dict['negerinnen'] = word_dict['negeren'] = 'neger'
word_dict['gastarbeitern'] = 'gastarbeiter'
word_dict['schwarzafrikas'] = 'schwarzafrika'
word_dict['liliputaners'] = 'liliputaner'
word_dict['zwergen'] = word_dict['zwerg'] = 'zwerg'
word_dict['südländers'] = word_dict['südländern'] = 'südländer'
word_dict['abendländischen'] = word_dict['abendländisch'] = 'abendland'




torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'de/lemma/gsd_charlm_customized.pt'))
