#!/bin/bash

# Скрипт для швидкого налаштування та запуску тестів (Linux/macOS)
# Quick Setup and Test Execution Script

echo "🚀 Quizizz Unit Tests - Quick Setup Script"
echo "=========================================="
echo ""

# Перевірка Python
echo "🔍 Перевірка Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python знайдено: $PYTHON_VERSION"
else
    echo "❌ Python не знайдено. Встановіть Python 3.9+ з https://www.python.org/"
    exit 1
fi

# Створення віртуального середовища
echo ""
echo "📦 Створення віртуального середовища..."
if [ -d "venv" ]; then
    echo "⚠️  Віртуальне середовище вже існує"
else
    python3 -m venv venv
    echo "✅ Віртуальне середовище створено"
fi

# Активація віртуального середовища
echo ""
echo "🔌 Активація віртуального середовища..."
source venv/bin/activate
echo "✅ Віртуальне середовище активовано"

# Оновлення pip
echo ""
echo "⬆️  Оновлення pip..."
python -m pip install --upgrade pip --quiet
echo "✅ pip оновлено"

# Встановлення залежностей
echo ""
echo "📚 Встановлення залежностей..."
pip install -r requirements.txt --quiet
echo "✅ Залежності встановлено"

# Створення директорії для звітів
echo ""
echo "📁 Створення директорії для звітів..."
if [ ! -d "reports" ]; then
    mkdir -p reports
    echo "✅ Директорія reports створена"
else
    echo "⚠️  Директорія reports вже існує"
fi

# Меню вибору дій
echo ""
echo "========================================"
echo "Оберіть дію:"
echo "========================================"
echo "1. Запустити всі тести (послідовно)"
echo "2. Запустити всі тести (паралельно)"
echo "3. Запустити тести з HTML звітом"
echo "4. Запустити тести з покриттям коду"
echo "5. Запустити тести з Allure звітом"
echo "6. Запустити BDD тести (Behave)"
echo "7. Запустити ВСЕ (повний CI/CD процес)"
echo "8. Перевірка коду (Pylint + Flake8)"
echo "9. Вийти"
echo ""

read -p "Введіть номер (1-9): " choice

case $choice in
    1)
        echo ""
        echo "🧪 Запуск тестів (послідовно)..."
        pytest tests/ -v
        ;;
    2)
        echo ""
        echo "⚡ Запуск тестів (паралельно)..."
        pytest tests/ -n auto -v
        ;;
    3)
        echo ""
        echo "📄 Запуск тестів з HTML звітом..."
        pytest tests/ -v --html=reports/report.html --self-contained-html
        echo ""
        echo "✅ Звіт створено: reports/report.html"
        read -p "Відкрити звіт? (y/n): " open_report
        if [ "$open_report" = "y" ]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open reports/report.html
            elif command -v open &> /dev/null; then
                open reports/report.html
            fi
        fi
        ;;
    4)
        echo ""
        echo "📊 Запуск тестів з покриттям коду..."
        pytest tests/ --cov=. --cov-report=html:reports/coverage --cov-report=term
        echo ""
        echo "✅ Звіт покриття створено: reports/coverage/index.html"
        read -p "Відкрити звіт покриття? (y/n): " open_coverage
        if [ "$open_coverage" = "y" ]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open reports/coverage/index.html
            elif command -v open &> /dev/null; then
                open reports/coverage/index.html
            fi
        fi
        ;;
    5)
        echo ""
        echo "📈 Запуск тестів з Allure звітом..."
        pytest tests/ --alluredir=reports/allure-results -v
        echo ""
        echo "✅ Allure результати створено: reports/allure-results"
        
        # Перевірка чи встановлено Allure
        if command -v allure &> /dev/null; then
            read -p "Згенерувати та відкрити Allure звіт? (y/n): " generate_allure
            if [ "$generate_allure" = "y" ]; then
                allure serve reports/allure-results
            fi
        else
            echo "⚠️  Allure commandline не встановлено"
            echo "   Linux: sudo apt-add-repository ppa:qameta/allure && sudo apt-get install allure"
            echo "   macOS: brew install allure"
        fi
        ;;
    6)
        echo ""
        echo "🥒 Запуск BDD тестів (Behave)..."
        if [ -d "tests/bdd/features" ]; then
            behave tests/bdd/features -v --format pretty
        else
            echo "⚠️  BDD тести не знайдено"
        fi
        ;;
    7)
        echo ""
        echo "🚀 Запуск ПОВНОГО CI/CD процесу..."
        echo ""
        
        echo "1️⃣ Перевірка коду..."
        pip install pylint flake8 --quiet
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        pylint *.py --exit-zero --output-format=text --reports=y > reports/pylint_report.txt
        
        echo ""
        echo "2️⃣ Unit тести (послідовно)..."
        pytest tests/ -v --html=reports/report_sequential.html --self-contained-html --junitxml=reports/junit_sequential.xml
        
        echo ""
        echo "3️⃣ Unit тести (паралельно)..."
        pytest tests/ -n auto -v --html=reports/report_parallel.html --self-contained-html --junitxml=reports/junit_parallel.xml
        
        echo ""
        echo "4️⃣ Покриття коду..."
        pytest tests/ --cov=. --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-report=term
        
        echo ""
        echo "5️⃣ Allure звіти..."
        pytest tests/ --alluredir=reports/allure-results -v
        
        echo ""
        echo "6️⃣ BDD тести..."
        if [ -d "tests/bdd/features" ]; then
            behave tests/bdd/features --junit --junit-directory reports/bdd
        fi
        
        echo ""
        echo "✅ ВСЕ ЗАВЕРШЕНО!"
        echo ""
        echo "📊 Звіти доступні в директорії: reports/"
        
        read -p "Відкрити папку зі звітами? (y/n): " open_reports_folder
        if [ "$open_reports_folder" = "y" ]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open reports
            elif command -v open &> /dev/null; then
                open reports
            fi
        fi
        ;;
    8)
        echo ""
        echo "🔍 Перевірка коду..."
        pip install pylint flake8 --quiet
        
        echo ""
        echo "=== Flake8 ==="
        flake8 . --count --statistics
        
        echo ""
        echo "=== Pylint ==="
        pylint *.py --output-format=text --reports=y
        ;;
    9)
        echo ""
        echo "👋 До побачення!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Невірний вибір. Спробуйте ще раз."
        ;;
esac

echo ""
echo "========================================"
echo "✅ Виконання завершено!"
echo "========================================"
