#!/bin/bash

export STANZA_RESOURCES_DIR="$HOME/stanza_resources/"
export VOCABULARIES_PATH="./vocabularies"

LANGUAGE="it"
TERMS_FILEPATH="./vocabularies/${LANGUAGE}_vocab_from_graph.csv"
SAVEPATH="./vocabularies/${LANGUAGE}_vocab_from_graph_processed.pickle"

python -m src.utils.preprocess_terms \
  --terms-filepath "$TERMS_FILEPATH" \
  --savepath "$SAVEPATH" \
  --language "$LANGUAGE"
