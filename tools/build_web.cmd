@echo off

if "%CI%" == "true" (
    pip install -r web/requirements.txt
)

python web/wikigen.py build
