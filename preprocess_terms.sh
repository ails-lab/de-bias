#!/bin/bash

export STANZA_RESOURCES_DIR="$HOME/stanza_resources/"
export VOCABULARIES_PATH="./vocabularies"

langs=("en" "de" "nl" "it" "fr")
for LANGUAGE in "${langs[@]}"; do
  TERMS_FILEPATH="./vocabularies/${LANGUAGE}_vocab_from_graph.csv"
  SAVEPATH="./vocabularies/${LANGUAGE}_vocab_from_graph_processed.pickle"
  python -m src.utils.preprocess_terms \
  --terms-filepath "$TERMS_FILEPATH" \
  --savepath "$SAVEPATH" \
  --language "$LANGUAGE"
done
#LANGUAGE="en"
## TERMS_FILEPATH="./vocabularies/${LANGUAGE}_vocab_from_graph.csv"
#TERMS_FILEPATH="./vocabularies/corporate_bodies_${LANGUAGE}.csv"
## SAVEPATH="./vocabularies/${LANGUAGE}_vocab_from_graph_processed.pickle"
#SAVEPATH="./vocabularies/corporate_bodies_${LANGUAGE}_processed.pickle"
#
#python -m src.utils.preprocess_terms \
#  --terms-filepath "$TERMS_FILEPATH" \
#  --savepath "$SAVEPATH" \
#  --language "$LANGUAGE"
