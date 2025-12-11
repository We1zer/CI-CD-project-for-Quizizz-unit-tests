@echo off
cd /d "C:\Users\taras\Desktop\5sem\Надійність апаратних систем\quizizz-ci-cd\unit_tests"
echo ========================================
echo CI/CD Test Runner
echo ========================================
echo.
echo Current directory: %CD%
echo.
echo Running all tests (except allure examples)...
echo.
python -m pytest tests/ --ignore=tests/test_allure_examples.py -v --tb=short
echo.
echo ========================================
echo Tests completed!
echo ========================================
pause
