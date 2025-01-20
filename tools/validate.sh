#!/bin/bash

find 'functions/' -name '*.yaml' -type f -print0 | xargs -0 -I {} tools/yajsv -s schemas/function.yaml {}
find 'articles/' -name '*.yaml' -type f -print0 | xargs -0 -I {} tools/yajsv -s schemas/article.yaml {}
