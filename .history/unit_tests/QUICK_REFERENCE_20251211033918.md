# 🚀 ШВИДКИЙ ДОВІДНИК КОМАНД

## 🔧 Початкове налаштування

```powershell
# Створення віртуального середовища
python -m venv venv

# Активація (Windows)
.\venv\Scripts\activate

# Активація (Linux/Mac)
source venv/bin/activate

# Встановлення залежностей
pip install -r requirements.txt

# Оновлення pip
python -m pip install --upgrade pip
```

---

## 🧪 Базові команди pytest

```powershell
# Запуск всіх тестів
pytest tests/

# З verbose виводом
pytest tests/ -v

# З виводом print statements
pytest tests/ -v -s

# Зупинка на першій помилці
pytest tests/ -x

# Запуск конкретного файлу
pytest tests/test_quiz_search.py

# Запуск конкретного тесту
pytest tests/test_quiz_search.py::test_basic_search

# Запуск тестів з маркером
pytest tests/ -m smoke
pytest tests/ -m regression
pytest tests/ -m "not slow"

# Показати найповільніші тести
pytest tests/ --durations=10

# Детальний traceback
pytest tests/ --tb=long
```

---

## ⚡ Паралельне виконання

```powershell
# pytest-xdist (рекомендовано)
pytest tests/ -n auto                    # Автоматично визначити CPU cores
pytest tests/ -n 4                       # 4 паралельних процеси
pytest tests/ -n auto --dist loadfile    # Розподіл за файлами

# pytest-parallel
pytest tests/ --workers auto
pytest tests/ --workers 4
pytest tests/ --tests-per-worker auto
```

---

## 📊 Звіти

### HTML звіти
```powershell
# Базовий HTML звіт
pytest tests/ --html=reports/report.html

# Self-contained (один файл)
pytest tests/ --html=reports/report.html --self-contained-html

# З CSS стилями
pytest tests/ --html=reports/report.html --css=custom.css
```

### Coverage звіти
```powershell
# HTML coverage
pytest tests/ --cov=. --cov-report=html:reports/coverage

# Terminal coverage
pytest tests/ --cov=. --cov-report=term

# XML coverage (для CI/CD)
pytest tests/ --cov=. --cov-report=xml:reports/coverage.xml

# Всі формати одночасно
pytest tests/ --cov=. --cov-report=html:reports/coverage --cov-report=xml --cov-report=term

# З missing lines
pytest tests/ --cov=. --cov-report=term-missing
```

### Allure звіти
```powershell
# Генерація Allure результатів
pytest tests/ --alluredir=reports/allure-results

# З очищенням попередніх результатів
pytest tests/ --alluredir=reports/allure-results --clean-alluredir

# Запуск Allure сервера
allure serve reports/allure-results

# Генерація HTML звіту
allure generate reports/allure-results -o reports/allure-report --clean

# Відкрити згенерований звіт
allure open reports/allure-report
```

### JUnit XML
```powershell
# Генерація JUnit XML (для Jenkins)
pytest tests/ --junitxml=reports/junit.xml
```

---

## 🥒 BDD тести (Behave)

```powershell
# Запуск всіх BDD тестів
behave tests/bdd/features

# З verbose виводом
behave tests/bdd/features -v

# З форматованим виводом
behave tests/bdd/features --format pretty

# Запуск конкретного feature
behave tests/bdd/features/quiz_search.feature

# З тегами
behave tests/bdd/features --tags=@smoke
behave tests/bdd/features --tags=@critical

# Без кольорів
behave tests/bdd/features --no-color

# З JUnit XML виводом
behave tests/bdd/features --junit --junit-directory reports/bdd

# З HTML звітом (потрібен behave-html-formatter)
behave tests/bdd/features -f html -o reports/bdd/report.html
```

---

## 🔍 Code Quality

### Pylint
```powershell
# Перевірка всіх .py файлів
pylint *.py

# З звітом
pylint *.py --reports=y

# Збереження в файл
pylint *.py --output-format=text > reports/pylint_report.txt

# Тільки помилки
pylint *.py --errors-only

# З конкретним рейтингом
pylint *.py --fail-under=8.0

# Ігнорування конкретних помилок
pylint *.py --disable=C0111,C0103
```

### Flake8
```powershell
# Базова перевірка
flake8 .

# З статистикою
flake8 . --count --statistics

# Тільки критичні помилки
flake8 . --select=E9,F63,F7,F82

# З показом коду
flake8 . --show-source

# З ігноруванням
flake8 . --ignore=E501,W503

# Макс довжина рядка
flake8 . --max-line-length=120

# Збереження в файл
flake8 . > reports/flake8_report.txt
```

---

## 🔄 Комбіновані команди

```powershell
# Повний CI/CD цикл
pytest tests/ -v --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml --cov=. --cov-report=html:reports/coverage --alluredir=reports/allure-results

# Швидкі smoke тести
pytest tests/ -m smoke -v -x

# Regression тести з звітом
pytest tests/ -m regression -v --html=reports/regression.html --self-contained-html

# Паралельні тести з coverage
pytest tests/ -n auto --cov=. --cov-report=term

# Все крім повільних тестів
pytest tests/ -m "not slow" -v
```

---

## 📦 Управління залежностями

```powershell
# Встановлення з requirements.txt
pip install -r requirements.txt

# Збереження поточних залежностей
pip freeze > requirements.txt

# Встановлення конкретного пакету
pip install pytest-xdist

# Оновлення пакету
pip install --upgrade pytest

# Видалення пакету
pip uninstall pytest-parallel

# Показати встановлені пакети
pip list

# Показати outdated пакети
pip list --outdated

# Показати інформацію про пакет
pip show pytest
```

---

## 🛠️ Jenkins CLI

```powershell
# Завантаження Jenkins CLI jar
Invoke-WebRequest -Uri http://localhost:8080/jnlpJars/jenkins-cli.jar -OutFile jenkins-cli.jar

# Запуск build
java -jar jenkins-cli.jar -s http://localhost:8080/ build Quizizz-Unit-Tests-CI-CD

# Перегляд статусу job
java -jar jenkins-cli.jar -s http://localhost:8080/ get-job Quizizz-Unit-Tests-CI-CD

# Перегляд console output
java -jar jenkins-cli.jar -s http://localhost:8080/ console Quizizz-Unit-Tests-CI-CD
```

---

## 🌐 Git команди

```powershell
# Ініціалізація репозиторію
git init

# Додавання файлів
git add .
git add unit_tests/

# Commit
git commit -m "Add CI/CD configuration"

# Додавання remote
git remote add origin https://github.com/username/quizizz-ci-cd.git

# Push
git push -u origin main

# Перевірка статусу
git status

# Перегляд змін
git diff

# Перегляд логів
git log --oneline

# Створення гілки
git checkout -b feature/ci-cd

# Злиття гілок
git merge feature/ci-cd
```

---

## 🐛 Debugging

```powershell
# Pytest з pdb debugger
pytest tests/ --pdb

# Зупинка на першій помилці з pdb
pytest tests/ -x --pdb

# Запуск з lf (last failed)
pytest tests/ --lf

# Запуск з ff (failed first)
pytest tests/ --ff

# Показати локальні змінні при помилці
pytest tests/ -l

# Traceback режими
pytest tests/ --tb=short    # Короткий traceback
pytest tests/ --tb=long     # Повний traceback
pytest tests/ --tb=line     # Одна лінія на тест
pytest tests/ --tb=no       # Без traceback

# Verbose вивід з деталями
pytest tests/ -vv
```

---

## 📊 Аналіз результатів

```powershell
# Показати test session duration
pytest tests/ --durations=0

# Показати найповільніші 10 тестів
pytest tests/ --durations=10

# Показати найповільніші setup/teardown
pytest tests/ --durations-min=1.0

# Показати покриття з missing lines
pytest tests/ --cov=. --cov-report=term-missing

# JSON звіт
pytest tests/ --json-report --json-report-file=reports/report.json
```

---

## 🔧 Корисні алієси (додайте в PowerShell profile)

```powershell
# Відкрити PowerShell profile
notepad $PROFILE

# Додайте ці функції:
function pytest-quick { pytest tests/ -v -x }
function pytest-all { pytest tests/ -v }
function pytest-parallel { pytest tests/ -n auto -v }
function pytest-coverage { pytest tests/ --cov=. --cov-report=html:reports/coverage }
function pytest-allure { pytest tests/ --alluredir=reports/allure-results -v }
function behave-all { behave tests/bdd/features -v }
function reports-open { Start-Process reports/report.html }
```

---

## 🎯 Швидкі сценарії

### Сценарій 1: Швидка перевірка перед commit
```powershell
pytest tests/ -m smoke -v -x
```

### Сценарій 2: Повна перевірка
```powershell
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Сценарій 3: CI/CD симуляція
```powershell
# Code quality
flake8 . --count --statistics
pylint *.py --reports=y

# Tests
pytest tests/ -v --junitxml=reports/junit.xml

# Coverage
pytest tests/ --cov=. --cov-report=html:reports/coverage

# Allure
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Сценарій 4: Performance test
```powershell
Write-Host "Sequential:"
Measure-Command { pytest tests/ -v }

Write-Host "`nParallel:"
Measure-Command { pytest tests/ -n auto -v }
```

---

## 💡 Поради

1. **Використовуйте маркери** для категоризації тестів
2. **Паралельне виконання** економить час (використовуйте -n auto)
3. **Coverage звіти** допомагають знайти непокритий код
4. **Allure звіти** найкращі для презентацій
5. **BDD тести** чудові для документації функціоналу
6. **-x флаг** економить час при debugging
7. **--lf флаг** запускає тільки провалені тести

---

**Збережіть цей довідник для швидкого доступу! 📖**
