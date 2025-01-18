@echo off

.\tools\yajsv.exe -s schemas/navigation.yaml "wiki/navigation.yaml"
.\tools\yajsv.exe -s schemas/categories.yaml "wiki/categories.yaml"

for /r "functions" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/function.yaml "%%f"
)

for /r "articles" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/article.yaml "%%f"
)
