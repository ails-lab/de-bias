import torch


model = torch.load('~/stanza_resources/en/lemma/combined_charlm.pt', map_location='cpu')
word_dict, composite_dict = model['dicts']

word_dict['woman'] = word_dict['women'] = 'man'
word_dict['chinkis'] = 'chinki'
word_dict['coolies'] = 'coolie'
word_dict['eyeties'] = 'eyetie'
word_dict['halfcastes'] = 'halfcaste'
word_dict['junkies'] = 'junkie'
word_dict['junky'] = 'junkie'
word_dict['holebis'] = 'holebi'
word_dict['curiosities'] = 'curiosities'
word_dict['krauts'] = 'kraut'
word_dict['roots'] = 'roots'
word_dict['showmen'] = word_dict['showwoman'] = word_dict['showwomen'] = 'showman'
word_dict['bombays'] = 'bombay'
word_dict['bushmen'] = word_dict['bushwoman'] = word_dict['bushwomen'] = 'bushman'
word_dict['chinamen'] = word_dict['chinawoman'] = word_dict['chinawomen'] = 'chinaman'
word_dict['dwarves'] = 'dwarf'
word_dict['fritzes'] = 'fritz'
word_dict['kulis'] = 'kuli'
word_dict['latina'] = word_dict['latinas'] = 'latino'
word_dict['muladis'] = 'muladi'
word_dict['negroes'] = 'negro'
word_dict['transes'] = 'trans'
word_dict['exotics'] = 'exotic'
word_dict['pakis'] = 'paki'
word_dict['pervs'] = 'perv'
word_dict['westerns'] = 'western'
word_dict['paraphilias'] = 'paraphilia'

composite_dict[('mixed', 'NOUN')] = composite_dict[('mixed', 'ADJ')] = 'mixed'
composite_dict[('features', 'NOUN')] = 'features'
composite_dict[('bent', 'NOUN')] = composite_dict[('bent', 'ADJ')] = 'bent'
composite_dict[('colored', 'NOUN')] = composite_dict[('colored', 'ADJ')] = 'colored'
composite_dict[('coloured', 'NOUN')] = composite_dict[('coloured', 'ADJ')] = 'coloured'

torch.save(model, '~/stanza_resources/en/lemma/combined_charlm_customized.pt')
