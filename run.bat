@echo off
python requirements_checker.py requirements.txt
if errorlevel 1 (
    echo packages not complete!
    echo Installing...
    pip install -r requirements.txt
)
python -m myreader %*
pause
