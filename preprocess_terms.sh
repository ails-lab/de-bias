#!/bin/bash

export STANZA_RESOURCES_DIR="$HOME/stanza_resources/"
export VOCABULARIES_PATH="./vocabularies"

langs=("en" "de" "nl" "it" "fr")
for LANGUAGE in "${langs[@]}"; do
  TERMS_FILEPATH="./vocabularies/${LANGUAGE}_published_vocab.csv"
  SAVEPATH="./vocabularies/${LANGUAGE}_published_vocab_processed.pickle"
  python -m src.utils.preprocess_terms \
  --terms-filepath "$TERMS_FILEPATH" \
  --savepath "$SAVEPATH" \
  --language "$LANGUAGE"
done


#LANGUAGE="en"
#TERMS_FILEPATH="./vocabularies/${LANGUAGE}_published_vocab.csv"
#SAVEPATH="./vocabularies/${LANGUAGE}_published_vocab_processed.pickle"
#python -m src.utils.preprocess_terms \
#  --terms-filepath "$TERMS_FILEPATH" \
#  --savepath "$SAVEPATH" \
#  --language "$LANGUAGE"
