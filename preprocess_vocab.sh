#!/bin/bash

export VOCABULARIES_PATH="./vocabularies"

langs=("en" "de" "nl" "it" "fr")
for LANGUAGE in "${langs[@]}"; do
  SAVEPATH="./vocabularies/${LANGUAGE}_published_vocab.csv"
  python -m src.utils.pull_vocab \
  --savepath "$SAVEPATH" \
  --language "$LANGUAGE"
  sleep 1
done
