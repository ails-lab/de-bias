#!/bin/bash

export VOCABULARIES_PATH="./vocabularies"

LANGUAGE="dutch"

python vocabulary_preprocessing/${LANGUAGE}_vocab_v2.py
