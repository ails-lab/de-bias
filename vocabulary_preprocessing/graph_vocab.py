import os
from collections import defaultdict

import pandas as pd
from rdflib import Graph
from rdflib.namespace import RDF, SKOS, DCTERMS


VOCABULARY_FILEPATHS = os.getenv('VOCABULARY_FILEPATHS').split(os.pathsep)


g = Graph()
for path in VOCABULARY_FILEPATHS:
    g.parse(path)
# g.parse(os.path.join(VOCABULARIES_PATH, '20240607-DE-BIAS-Vocabulary-Terms.ttl'))
# g.parse(os.path.join(VOCABULARIES_PATH, '20240607-DE-BIAS-Vocabulary-Issues.ttl'))
namespaces = dict(g.namespaces())

issue_with_term = list(g.subject_objects(
    predicate=namespaces['debias'] + 'contentiousTerm')
)

vocabularies = defaultdict(list)
for issue, term in issue_with_term:
    context = next(g.objects(subject=issue, predicate=DCTERMS + 'description'))

    disambiguation = bool(next(g.objects(subject=term, predicate=SKOS + 'editorialNote'), None))
    term_literal = next(g.objects(subject=term, predicate=namespaces['skosxl'] + 'literalForm'))
    vocabularies[term_literal.language].append(
        (str(term), str(term_literal), str(context), disambiguation))

dfs = {}
for lang, vocab in vocabularies.items():
    dfs[lang] = pd.DataFrame(vocab, columns=['uri', 'term', 'context', 'disambiguation'])

for k, v in dfs.items():
    with open('./vocabularies/{}_vocab_from_graph.csv'.format(k), 'wt') as fp:
        v.to_csv(fp, index=False, quoting=1)
