import torch
import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')

model = torch.load(os.path.join(STANZA_RESOURCES_DIR, 'nl/lemma/alpino_charlm.pt'), map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['woudje'] = 'woudje'
word_dict['diaspora'] = 'diaspora'
word_dict['aidspatiënt'] = word_dict['aidspatiënten'] = 'aidspatiënt'
word_dict['bosneger'] = 'bosneger'
word_dict['cultuurchristen'] = 'cultuurchristen'
word_dict['empowerment'] = 'empowerment'
word_dict['jappenkamp'] = 'jappenkamp'
word_dict['gekleurd'] = 'gekleurd'
word_dict['kroezelkop'] = 'kroezelkop'
word_dict['laaggeschoold'] = 'laaggeschoold'
word_dict['leefgebied'] = 'leefgebied'
word_dict['melaatse'] = 'melaatse'
word_dict['muzulvrouw'] = 'muzulvrouw'
word_dict['omaatje'] = 'omaatje'
word_dict['oudje'] = 'oudje'
word_dict['paaps'] = 'paaps'
word_dict['santenboetiek'] = 'santenboetiek'
word_dict['sloppenbewoner'] = 'sloppenbewoner'
word_dict['superstitie'] = 'superstitie'
word_dict['toverbeeld'] = 'toverbeeld'
word_dict['tropen'] = 'tropen'
word_dict['westers'] = 'westers'
word_dict['papistisch'] = 'papist'
word_dict['spleetogen'] = 'spleetoog'
word_dict['tzigane'] = 'tzigaan'
word_dict['zwartje'] = 'zwartje'
word_dict['évolués'] = word_dict['évolué'] = 'evolué'
word_dict['gehoorgestoord'] = 'gehoorgestoord'
word_dict['gehoorgestoorde'] = 'gehoorgestoord'
word_dict['gehoorgestoorden'] = 'gehoorgestoorden'
word_dict['inlandse'] = 'inlander'
word_dict['kalotten'] = 'karloot'
word_dict['magische'] = 'magie'

torch.save(model, os.path.join(STANZA_RESOURCES_DIR, 'nl/lemma/alpino_charlm_customized.pt'))
