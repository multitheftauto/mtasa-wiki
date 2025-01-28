@echo off

for /r "functions" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/function.yaml "%%f"
)

for /r "elements" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/element.yaml "%%f"
)

for /r "articles" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/article.yaml "%%f"
)
