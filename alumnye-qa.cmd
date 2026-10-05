@echo off
rem Single entry point:  alumnye-qa run --product=alumnye --platform=android --module=auth
set "PYTHONPATH=%~dp0source\mobile\alumnye"
set PYTHONIOENCODING=utf-8
python -m alumnye_qa %*
