#!/bin/bash

if [ "$CI" = "true" ]; then
    pip install -r web/requirements.txt
fi

python web/wikigen.py build
