import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'it/lemma/combined_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['mongoloidi'] = 'mongoloide'
word_dict['checche'] = 'checca'
word_dict['bastarda'] = 'bastarda'
word_dict['storpi'] = 'storpio'
word_dict['sodomita'] = 'sodomita'
word_dict['omofili'] = 'omofilo'
word_dict['giudea'] = 'giudea'
word_dict['terrona'] = 'terrona'
word_dict['zoppa'] = 'zoppa'

torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'it/lemma/combined_charlm_customized.pt'))
