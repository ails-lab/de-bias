import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'fr/lemma/combined_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['boys'] = word_dict['boyesse'] = word_dict['boyesses'] = 'boy'
word_dict['évolué'] = word_dict['évolués'] = word_dict['évoluée'] = word_dict['évoluées'] = 'evolué'
word_dict['nègres'] = 'nègre'
word_dict['enjuivées'] = 'enjuiver'
word_dict['asiates'] = 'asiate'
word_dict['travelos'] = 'travelo'
word_dict['féminazie'] = 'féminazi'
word_dict['niacouées'] = 'niacoué'
word_dict['niacoués'] = 'niacoué'
word_dict['bougnouls'] = 'bougnoule'
word_dict['bicotte'] = 'bicot'

composite_dict[('évolué', 'VERB')] = 'evolué'
composite_dict[('racisée', 'VERB')] = 'racisée'
composite_dict[('roms', 'NOUN')] = 'roms'

torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'fr/lemma/combined_charlm_customized.pt'))
