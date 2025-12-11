@echo off
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Running tests...
python -m pytest tests/ --ignore=tests/test_allure_examples.py -v
pause
