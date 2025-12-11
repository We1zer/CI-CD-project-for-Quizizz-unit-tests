# 🚀 Quizizz CI/CD Project - Unit Tests

Комплексний CI/CD проект для автоматизованого тестування Quizizz фреймворку з Jenkins, GitHub Actions, Allure та BDD.

## 📋 Огляд

Цей проект демонструє повну реалізацію CI/CD пайплайну для Python unit тестів з:
- ✅ **Jenkins Pipeline** з автоматичними тригерами
- ✅ **GitHub Actions** для CI/CD в хмарі
- ✅ **Паралельне виконання тестів** (pytest-xdist)
- ✅ **Allure Reports** для красивої звітності
- ✅ **BDD тести** (Behave framework)
- ✅ **Code Coverage** аналіз
- ✅ **Code Quality** перевірки (Pylint, Flake8)

## 🎯 Статистика проекту

- **159 Unit тестів** у 14 тестових файлах
- **2 BDD feature файли** з 8 сценаріями
- **Покриття функціоналу**: Quiz Search, Library, Categories, DSL
- **Підтримка паралельного запуску**: до 10x швидше

## 🏗️ Структура проекту

```
unit_tests/
├── 📄 Jenkinsfile                    # Jenkins Pipeline конфігурація
├── 📄 pytest.ini                     # Pytest налаштування
├── 📄 allure.yml                     # Allure конфігурація
├── 📄 requirements.txt               # Python залежності
├── 📄 CI_CD_SETUP.md                # Повна документація налаштування
├── 📄 JENKINS_SETUP.txt             # Jenkins інструкції
├── 📄 setup_and_run.ps1             # Скрипт швидкого запуску
│
├── 📁 tests/                         # Тестові файли
│   ├── test_*.py                     # 14 тестових файлів (159 тестів)
│   ├── test_allure_examples.py       # Приклади Allure анотацій
│   └── bdd/                          # BDD тести
│       ├── features/                 # Gherkin feature файли
│       │   ├── quiz_search.feature
│       │   └── quiz_library.feature
│       ├── steps/                    # Step definitions
│       │   └── quiz_steps.py
│       └── environment.py            # Behave конфігурація
│
├── 📁 reports/                       # Директорія для звітів
│   ├── allure-results/              # Allure дані
│   ├── coverage/                     # Coverage HTML звіти
│   ├── bdd/                          # BDD JUnit звіти
│   └── *.html, *.xml                # Різні звіти
│
└── 📁 mock_data/                    # Тестові дані
    ├── search_results.json
    └── category_tree.json
```

## 🚀 Швидкий старт

### Метод 1: Використання PowerShell скрипту (Рекомендовано)

```powershell
cd unit_tests
.\setup_and_run.ps1
```

Скрипт автоматично:
1. Перевірить Python
2. Створить віртуальне середовище
3. Встановить залежності
4. Покаже меню з опціями запуску

### Метод 2: Ручне налаштування

```powershell
# 1. Створення віртуального середовища
cd unit_tests
python -m venv venv
.\venv\Scripts\activate

# 2. Встановлення залежностей
pip install -r requirements.txt

# 3. Запуск тестів
pytest tests/ -v

# 4. Запуск з HTML звітом
pytest tests/ -v --html=reports/report.html --self-contained-html

# 5. Паралельний запуск
pytest tests/ -n auto -v

# 6. З покриттям коду
pytest tests/ --cov=. --cov-report=html:reports/coverage

# 7. З Allure звітом
pytest tests/ --alluredir=reports/allure-results -v
allure serve reports/allure-results
```

## 🔧 Налаштування Jenkins

### Крок 1: Встановлення Jenkins

1. Завантажте Jenkins: https://www.jenkins.io/download/
2. Встановіть та запустіть
3. Відкрийте: http://localhost:8080
4. Введіть початковий пароль адміністратора

### Крок 2: Встановлення плагінів

**Manage Jenkins → Manage Plugins → Available**

Необхідні плагіни:
- Git Plugin
- Pipeline
- HTML Publisher
- Allure Jenkins Plugin
- JUnit Plugin

### Крок 3: Створення Pipeline Job

1. **New Item** → Введіть назву → **Pipeline** → OK
2. **Pipeline** секція:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `ваш-репозиторій`
   - Script Path: `unit_tests/Jenkinsfile`
3. **Build Triggers**:
   - ✓ Poll SCM: `H/5 * * * *`
   - ✓ Build periodically: `0 2 * * *`

### Детальні інструкції

Дивіться: [`JENKINS_SETUP.txt`](JENKINS_SETUP.txt) та [`CI_CD_SETUP.md`](CI_CD_SETUP.md)

## 🌐 GitHub Actions

GitHub Actions автоматично налаштовано у `.github/workflows/unit_tests_ci.yml`

### Автоматичний запуск при:
- 📤 Push до main/develop гілки
- 🔀 Pull Request
- 🕐 Щоденно о 2:00 UTC
- 🖱️ Ручний запуск (workflow_dispatch)

### Що виконується:
1. Тести на різних OS (Ubuntu, Windows)
2. Тести на різних версіях Python (3.9, 3.10, 3.11)
3. Code Quality перевірки
4. Паралельні тести
5. Coverage звіти
6. Allure звіти → GitHub Pages

### Перегляд результатів:
- Перейдіть на вкладку **Actions** у вашому GitHub репозиторії
- Allure звіт: `https://ваш-username.github.io/quizizz-ci-cd/`

## 📊 Звітність

### Allure Reports
```powershell
# Генерація та відкриття
pytest tests/ --alluredir=reports/allure-results -v
allure serve reports/allure-results
```

**Features:**
- 📈 Красиві графіки та діаграми
- 📊 Тренди виконання тестів
- 🔍 Детальні кроки тестів
- 📎 Attachments та screenshots
- 🏷️ Категоризація по features/stories

### HTML Reports
```powershell
pytest tests/ --html=reports/report.html --self-contained-html
```

### Coverage Reports
```powershell
pytest tests/ --cov=. --cov-report=html:reports/coverage
```

## ⚡ Паралельне виконання

### pytest-xdist (Рекомендовано)
```powershell
# Автоматично визначити кількість ядер
pytest tests/ -n auto

# Конкретна кількість workers
pytest tests/ -n 4

# З розподілом за файлами
pytest tests/ -n auto --dist loadfile
```

### Порівняння швидкості:
- **Sequential**: ~30 секунд
- **Parallel (4 cores)**: ~8 секунд
- **Speedup**: ~3.75x

## 🥒 BDD тести (Behave)

### Запуск BDD тестів
```powershell
cd unit_tests
behave tests/bdd/features -v
```

### Структура BDD тестів:
```
tests/bdd/
├── features/
│   ├── quiz_search.feature      # Сценарії пошуку (4 сценарії)
│   └── quiz_library.feature     # Сценарії бібліотеки (4 сценарії)
├── steps/
│   └── quiz_steps.py            # 40+ step definitions
└── environment.py               # Hooks та конфігурація
```

### Приклад Feature:
```gherkin
# language: uk
Функціонал: Пошук квізів у Quizizz

  Сценарій: Успішний пошук квізу за назвою
    Дано я відкрив сторінку пошуку Quizizz
    Коли я введу "Python Programming" в поле пошуку
    І натисну кнопку "Пошук"
    Тоді я побачу список квізів з результатами
```

## 🔍 Code Quality

### Pylint
```powershell
pylint *.py --output-format=text --reports=y
```

### Flake8
```powershell
flake8 . --count --statistics
```

## 📦 Залежності

```
pytest>=7.4.0              # Тестовий фреймворк
pytest-xdist>=3.3.1        # Паралельне виконання
pytest-html>=3.2.0         # HTML звіти
pytest-cov>=4.1.0          # Coverage
allure-pytest>=2.13.2      # Allure інтеграція
behave>=1.2.6              # BDD фреймворк
pylint>=2.17.5             # Code quality
flake8>=6.0.0              # Linter
```

## 🎓 Навчальні матеріали

### Документація:
- [`CI_CD_SETUP.md`](CI_CD_SETUP.md) - Повна інструкція по налаштуванню
- [`JENKINS_SETUP.txt`](JENKINS_SETUP.txt) - Jenkins конфігурація
- [`tests/test_allure_examples.py`](tests/test_allure_examples.py) - Приклади Allure

### Корисні команди:
```powershell
# Запуск конкретного тесту
pytest tests/test_quiz_search.py::test_basic_search -v

# Запуск з маркерами
pytest tests/ -m smoke -v
pytest tests/ -m "not slow" -v

# Verbose вивід з принтами
pytest tests/ -v -s

# Зупинка на першій помилці
pytest tests/ -x

# Показати найповільніші тести
pytest tests/ --durations=10
```

## 🛠️ Troubleshooting

### Python не знайдено
```powershell
# Додайте Python до PATH або використайте повний шлях
C:\Python39\python.exe -m pytest tests/
```

### Віртуальне середовище не активується
```powershell
# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Jenkins не може знайти Python
- Додайте Python до системного PATH
- Або налаштуйте в Global Tool Configuration
- Або використайте повний шлях в Jenkinsfile

### Allure commandline не встановлено
```powershell
# Windows (через Scoop)
scoop install allure

# macOS
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

## 📈 Метрики проекту

- **Тестове покриття**: 159 тестів
- **BDD сценарії**: 8 сценаріїв
- **Підтримувані OS**: Windows, Linux, macOS
- **Підтримувані Python версії**: 3.9, 3.10, 3.11
- **Час виконання (sequential)**: ~30s
- **Час виконання (parallel)**: ~8s

## 🤝 Внесок

Цей проект створено як навчальний приклад CI/CD для курсу "Надійність апаратних систем".

## 📞 Підтримка

Для питань створюйте Issue в репозиторії.

---

**Успіхів з автоматизацією тестування! 🚀**
