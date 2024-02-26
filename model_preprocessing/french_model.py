import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'fr/lemma/combined_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['boys'] = word_dict['boyesse'] = word_dict['boyesses'] = 'boy'
word_dict['évolué'] = word_dict['évolués'] = word_dict['évoluée'] = word_dict['évoluées'] = 'évolué'

composite_dict[('évolué', 'VERB')] = 'évolué'

torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'fr/lemma/combined_charlm_customized.pt'))
