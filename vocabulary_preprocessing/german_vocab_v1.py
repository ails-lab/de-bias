import pandas as pd
import os


VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

df = pd.read_csv(os.path.join(VOCABULARIES_PATH,
                              'DE-BIAS Vocabulary v1 for review - Deutsch.csv'),
                 dtype={'Contentious labels': str})
terms = df['Contentious labels']

terms.to_csv(os.path.join(VOCABULARIES_PATH,
                          'DE-BIAS Vocabulary v1 for review - Deutsch_clean.csv'),
             index=False, header=False, quoting=1)
