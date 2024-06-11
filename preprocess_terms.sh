#!/bin/bash

export STANZA_RESOURCES_DIR="$HOME/stanza_resources/"
export VOCABULARIES_PATH="./vocabularies"

TERMS_FILEPATH="./vocabularies/DE-BIAS Vocabulary v2 - Nederlands_clean.csv"
SAVEPATH="./vocabularies/english_vocab_v2_processed.pickle"
LANGUAGE="nl"

python -m src.utils.preprocess_terms \
  --terms-filepath "$TERMS_FILEPATH" \
  --savepath "$SAVEPATH" \
  --language "$LANGUAGE"
