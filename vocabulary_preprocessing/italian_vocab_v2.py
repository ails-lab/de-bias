import pandas as pd
import os


VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

df = pd.read_csv(os.path.join(VOCABULARIES_PATH, 'DE-BIAS Vocabulary v2 - Italiano.csv'),
                 dtype={'Contentious labels': str})

df['ID'] = df['Contentious labels']
del df['Status'], df['Suggestion description'], df['Suggested alternatives']
del df['Source'], df['Link / reference']
del df['Added By'], df['Remarks'], df['word count contentious issue description']
del df['Long versions contentious issues']
df['Disambiguation needed?'][~ df['Disambiguation needed?'].isna()] = True
df['Disambiguation needed?'][df['Disambiguation needed?'].isna()] = False
df = df.rename(columns={'ID': 'uri',
                        'Contentious issue': 'context',
                        'Contentious labels': 'term',
                        'Disambiguation needed?': 'disambiguation'})
df = df.dropna()
df.to_csv(os.path.join(VOCABULARIES_PATH,
                       'DE-BIAS Vocabulary v2 - Italiano_clean.csv'),
          index=False, quoting=1)
