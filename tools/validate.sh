#!/bin/bash

exit_code=0

find 'functions/' -name "*.yaml" -type f | while read -r file; do
    tools/yajsv -s schemas/function.yaml "$file"
    
    if [ $? -ne 0 ]; then
        exit_code=1
    fi
done

exit $exit_code
