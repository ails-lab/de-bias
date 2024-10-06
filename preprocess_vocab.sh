#!/bin/bash

#export VOCABULARIES_PATH="./vocabularies"
#VOCABULARY_FILEPATHS="./vocabularies/20240607-DE-BIAS-Vocabulary-Terms.ttl"
#VOCABULARY_FILEPATHS="$VOCABULARY_FILEPATHS:./vocabularies/20240607-DE-BIAS-Vocabulary-Issues.ttl"
#export VOCABULARY_FILEPATHS

export VOCABULARY_FILEPATHS="./vocabularies/20240906-DE-BIAS-Vocabulary-Terms-and-issues_French-addition.ttl"

python vocabulary_preprocessing/graph_vocab.py
