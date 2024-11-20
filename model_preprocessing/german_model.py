import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'de/lemma/gsd_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['mohren'] = 'mohr'
word_dict['liliputanerin'] = 'liliputaner'
word_dict['muselmänner'] = 'muselmann'
word_dict['üdländerin'] = 'südländer'
word_dict['brunnenvergifterin'] = 'brunnenvergifter'
word_dict['brunnenvergifterinnen'] = 'brunnenvergifter'
word_dict['pygmäinnen'] = 'pygmäin'
word_dict['halbjüdinnen'] = 'halbjüdin'
word_dict['mestinzinnen'] = 'mestinzin'
word_dict['kanaken'] = 'kanake'
word_dict['hottentotten'] = 'hottentotte'
word_dict['androgyne'] = 'androgyn'
word_dict['mongoloide'] = 'mongoloid'


torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'de/lemma/gsd_charlm_customized.pt'))
