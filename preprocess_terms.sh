#!/bin/bash

export STANZA_RESOURCES_DIR="$HOME/stanza_resources/"
export VOCABULARIES_PATH="./vocabularies"

LANGUAGE="nl"
TERMS_FILEPATH="./vocabularies/${LANGUAGE}_fake_vocab.csv"
SAVEPATH="./vocabularies/${LANGUAGE}_fake_vocab_processed.pickle"

python -m src.utils.preprocess_terms \
  --terms-filepath "$TERMS_FILEPATH" \
  --savepath "$SAVEPATH" \
  --language "$LANGUAGE"
