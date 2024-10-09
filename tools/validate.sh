#!/bin/bash

find 'functions/' -name '*.yaml' -type f -print0 | xargs -0L1 tools/yajsv -s schemas/function.yaml
