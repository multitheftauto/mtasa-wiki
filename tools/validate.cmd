@echo off

for /r "functions" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/function.yaml "%%f"
)

for /r "elements" %%f in (*.yaml) do (
    .\tools\yajsv.exe -s schemas/element.yaml "%%f"
)

@REM for /r "events" %%f in (*.yaml) do (
@REM     .\tools\yajsv.exe -s schemas/events.yaml "%%f"
@REM )
