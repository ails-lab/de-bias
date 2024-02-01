import pandas as pd
import os


VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

df = pd.read_csv(os.path.join(VOCABULARIES_PATH, 'DE-BIAS Vocabulary v1 for review - English.csv'),
                 dtype={'Contentious labels': str})
terms = df['Contentious labels']
terms = terms.dropna()

# Drop first entry which is (((echo))). This will be matched with a regex, not the vocabulary.
terms = terms.drop(0)
terms = terms.replace(to_replace='chink/s', value='chink')
terms = terms.replace(to_replace='chinki (South Asia)', value='chinki')
terms = terms.replace(to_replace='Closet (be in)', value='in the closet')
terms = pd.concat([terms, pd.Series(['closeted'])], ignore_index=True)
terms = terms.replace(to_replace='kuli/s', value='kuli')
terms = terms.replace(to_replace='skin colour/s', value='skin colour')
terms = pd.concat([terms, pd.Series(['skin color'])], ignore_index=True)
terms = pd.concat([terms, pd.Series(['coloured'])], ignore_index=True)
terms.to_csv(os.path.join(VOCABULARIES_PATH,
                          'DE-BIAS Vocabulary v1 for review - English_clean.csv'),
             index=False, header=False, quoting=1)
