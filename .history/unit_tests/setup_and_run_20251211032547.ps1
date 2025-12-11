# Скрипт для швидкого налаштування та запуску тестів
Write-Host "🚀 Quizizz Unit Tests - Quick Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Перевірка Python
Write-Host "🔍 Перевірка Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python знайдено: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python не знайдено. Встановіть Python 3.9+ з https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Створення віртуального середовища
Write-Host ""
Write-Host "📦 Створення віртуального середовища..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Віртуальне середовище вже існує" -ForegroundColor Yellow
}
else {
    python -m venv venv
    Write-Host "✅ Віртуальне середовище створено" -ForegroundColor Green
}

# Активація віртуального середовища
Write-Host ""
Write-Host "🔌 Активація віртуального середовища..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Віртуальне середовище активовано" -ForegroundColor Green

# Оновлення pip
Write-Host ""
Write-Host "⬆️  Оновлення pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✅ pip оновлено" -ForegroundColor Green

# Встановлення залежностей
Write-Host ""
Write-Host "📚 Встановлення залежностей..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Залежності встановлено" -ForegroundColor Green

# Створення директорії для звітів
Write-Host ""
Write-Host "📁 Створення директорії для звітів..." -ForegroundColor Yellow
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" -Force | Out-Null
    Write-Host "✅ Директорія reports створена" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Директорія reports вже існує" -ForegroundColor Yellow
}

# Меню вибору дій
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Оберіть дію:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Запустити всі тести (послідовно)" -ForegroundColor White
Write-Host "2. Запустити всі тести (паралельно)" -ForegroundColor White
Write-Host "3. Запустити тести з HTML звітом" -ForegroundColor White
Write-Host "4. Запустити тести з покриттям коду" -ForegroundColor White
Write-Host "5. Запустити тести з Allure звітом" -ForegroundColor White
Write-Host "6. Запустити BDD тести (Behave)" -ForegroundColor White
Write-Host "7. Запустити ВСЕ (повний CI/CD процес)" -ForegroundColor White
Write-Host "8. Перевірка коду (Pylint + Flake8)" -ForegroundColor White
Write-Host "9. Вийти" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Введіть номер (1-9)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🧪 Запуск тестів (послідовно)..." -ForegroundColor Yellow
        pytest tests/ -v
    }
    "2" {
        Write-Host ""
        Write-Host "⚡ Запуск тестів (паралельно)..." -ForegroundColor Yellow
        pytest tests/ -n auto -v
    }
    "3" {
        Write-Host ""
        Write-Host "📄 Запуск тестів з HTML звітом..." -ForegroundColor Yellow
        pytest tests/ -v --html=reports/report.html --self-contained-html
        Write-Host ""
        Write-Host "✅ Звіт створено: reports/report.html" -ForegroundColor Green
        $openReport = Read-Host "Відкрити звіт? (y/n)"
        if ($openReport -eq "y") {
            Start-Process "reports/report.html"
        }
    }
    "4" {
        Write-Host ""
        Write-Host "📊 Запуск тестів з покриттям коду..." -ForegroundColor Yellow
        pytest tests/ --cov=. --cov-report=html:reports/coverage --cov-report=term
        Write-Host ""
        Write-Host "✅ Звіт покриття створено: reports/coverage/index.html" -ForegroundColor Green
        $openCoverage = Read-Host "Відкрити звіт покриття? (y/n)"
        if ($openCoverage -eq "y") {
            Start-Process "reports/coverage/index.html"
        }
    }
    "5" {
        Write-Host ""
        Write-Host "📈 Запуск тестів з Allure звітом..." -ForegroundColor Yellow
        pytest tests/ --alluredir=reports/allure-results -v
        Write-Host ""
        Write-Host "✅ Allure результати створено: reports/allure-results" -ForegroundColor Green
        
        try {
            $null = Get-Command allure -ErrorAction Stop
            $generateAllure = Read-Host "Згенерувати та відкрити Allure звіт? (y/n)"
            if ($generateAllure -eq "y") {
                allure serve reports/allure-results
            }
        }
        catch {
            Write-Host "⚠️  Allure commandline не встановлено" -ForegroundColor Yellow
            Write-Host "   Встановіть через Scoop: scoop install allure" -ForegroundColor Yellow
        }
    }
    "6" {
        Write-Host ""
        Write-Host "🥒 Запуск BDD тестів (Behave)..." -ForegroundColor Yellow
        if (Test-Path "tests/bdd/features") {
            behave tests/bdd/features -v --format pretty
        }
        else {
            Write-Host "⚠️  BDD тести не знайдено" -ForegroundColor Yellow
        }
    }
    "7" {
        Write-Host ""
        Write-Host "🚀 Запуск ПОВНОГО CI/CD процесу..." -ForegroundColor Yellow
        Write-Host ""
        
        Write-Host "1️⃣ Перевірка коду..." -ForegroundColor Cyan
        pip install pylint flake8 --quiet
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        pylint *.py --exit-zero --output-format=text --reports=y > reports/pylint_report.txt
        
        Write-Host ""
        Write-Host "2️⃣ Unit тести (послідовно)..." -ForegroundColor Cyan
        pytest tests/ -v --html=reports/report_sequential.html --self-contained-html --junitxml=reports/junit_sequential.xml
        
        Write-Host ""
        Write-Host "3️⃣ Unit тести (паралельно)..." -ForegroundColor Cyan
        pytest tests/ -n auto -v --html=reports/report_parallel.html --self-contained-html --junitxml=reports/junit_parallel.xml
        
        Write-Host ""
        Write-Host "4️⃣ Покриття коду..." -ForegroundColor Cyan
        pytest tests/ --cov=. --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-report=term
        
        Write-Host ""
        Write-Host "5️⃣ Allure звіти..." -ForegroundColor Cyan
        pytest tests/ --alluredir=reports/allure-results -v
        
        Write-Host ""
        Write-Host "6️⃣ BDD тести..." -ForegroundColor Cyan
        if (Test-Path "tests/bdd/features") {
            behave tests/bdd/features --junit --junit-directory reports/bdd
        }
        
        Write-Host ""
        Write-Host "✅ ВСЕ ЗАВЕРШЕНО!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Звіти доступні в директорії: reports/" -ForegroundColor Cyan
        
        $openReportsFolder = Read-Host "Відкрити папку зі звітами? (y/n)"
        if ($openReportsFolder -eq "y") {
            Invoke-Item "reports"
        }
    }
    "8" {
        Write-Host ""
        Write-Host "🔍 Перевірка коду..." -ForegroundColor Yellow
        pip install pylint flake8 --quiet
        
        Write-Host ""
        Write-Host "=== Flake8 ===" -ForegroundColor Cyan
        flake8 . --count --statistics
        
        Write-Host ""
        Write-Host "=== Pylint ===" -ForegroundColor Cyan
        pylint *.py --output-format=text --reports=y
    }
    "9" {
        Write-Host ""
        Write-Host "👋 До побачення!" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "❌ Невірний вибір. Спробуйте ще раз." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Виконання завершено!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
