@echo off

for /r "functions" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/function.yaml "%%f"
)
