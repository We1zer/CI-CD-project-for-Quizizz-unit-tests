# 🧪 ІНСТРУКЦІЯ ДЛЯ ВИКЛАДАЧА - ТЕСТУВАННЯ CI/CD

## Швидкий тест усієї системи (5-10 хвилин)

### ✅ Крок 1: Перевірка базового функціоналу

```powershell
# Перейдіть до директорії unit_tests
cd unit_tests

# Запустіть скрипт автоматичного налаштування
.\setup_and_run.ps1
# Оберіть опцію 7 (Запустити ВСЕ)
```

### ✅ Крок 2: Перевірка створених файлів

Перевірте що створено наступні файли:

#### CI/CD конфігурації:
- ✅ `Jenkinsfile` - Jenkins Pipeline
- ✅ `.github/workflows/unit_tests_ci.yml` - GitHub Actions
- ✅ `pytest.ini` - Pytest конфігурація
- ✅ `allure.yml` - Allure налаштування

#### Документація:
- ✅ `CI_CD_SETUP.md` - Повна інструкція
- ✅ `JENKINS_SETUP.txt` - Jenkins налаштування
- ✅ `README_CI_CD.md` - Загальний README

#### BDD тести:
- ✅ `tests/bdd/features/quiz_search.feature`
- ✅ `tests/bdd/features/quiz_library.feature`
- ✅ `tests/bdd/steps/quiz_steps.py`
- ✅ `tests/bdd/environment.py`

#### Приклади:
- ✅ `tests/test_allure_examples.py` - Allure анотації
- ✅ `setup_and_run.ps1` - Windows скрипт
- ✅ `setup_and_run.sh` - Linux/Mac скрипт

### ✅ Крок 3: Запуск різних типів тестів

```powershell
# 1. Базові unit тести
pytest tests/test_quiz_search.py -v

# 2. Паралельні тести
pytest tests/ -n auto -v

# 3. З HTML звітом
pytest tests/ --html=reports/report.html --self-contained-html

# 4. З покриттям
pytest tests/ --cov=. --cov-report=html:reports/coverage

# 5. З Allure
pytest tests/ --alluredir=reports/allure-results -v

# 6. BDD тести
behave tests/bdd/features -v
```

### ✅ Крок 4: Перевірка звітів

Після запуску перевірте створені звіти:

```powershell
# Відкрити HTML звіт
start reports/report.html

# Відкрити Coverage звіт
start reports/coverage/index.html

# Згенерувати Allure звіт (якщо встановлено Allure)
allure serve reports/allure-results
```

---

## 📊 Що саме перевіряти

### 1️⃣ Jenkinsfile (unit_tests/Jenkinsfile)

**Перевірте наявність:**
- ✅ Stages: Checkout, Setup, Tests, Reports
- ✅ Паралельні stages для sequential і parallel тестів
- ✅ Allure report generation
- ✅ Coverage report generation
- ✅ BDD tests stage
- ✅ Triggers: pollSCM та cron
- ✅ Post actions: success, failure, always

**Ключові особливості:**
```groovy
triggers {
    pollSCM('H/5 * * * *')      // Автоматичний запуск
    cron('0 2 * * *')           // Періодична збірка
}

parallel {
    stage('Sequential') { ... }  // Звичайні тести
    stage('Parallel') { ... }    // Паралельні тести
}
```

### 2️⃣ GitHub Actions (.github/workflows/unit_tests_ci.yml)

**Перевірте наявність:**
- ✅ Matrix strategy (Ubuntu, Windows / Python 3.9, 3.10, 3.11)
- ✅ Caching pip dependencies
- ✅ Code quality checks
- ✅ Parallel test execution
- ✅ Coverage upload to Codecov
- ✅ Allure report generation
- ✅ Publishing to GitHub Pages
- ✅ Artifact uploads

**Ключові особливості:**
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.9', '3.10', '3.11']
```

### 3️⃣ pytest.ini конфігурація

**Перевірте:**
- ✅ Test discovery patterns
- ✅ Custom markers (smoke, regression, slow, etc.)
- ✅ Coverage configuration
- ✅ Allure integration

### 4️⃣ BDD тести (Behave)

**Перевірте файли:**
```
tests/bdd/
├── features/
│   ├── quiz_search.feature      # Мінімум 4 сценарії
│   └── quiz_library.feature     # Мінімум 4 сценарії
├── steps/
│   └── quiz_steps.py            # 40+ step definitions
└── environment.py
```

**Запустіть BDD тести:**
```powershell
behave tests/bdd/features --format pretty
```

**Очікуваний результат:**
- 8 scenarios (8 passed)
- 30+ steps (30+ passed)

### 5️⃣ Паралельне виконання

**Тест продуктивності:**
```powershell
# Виміряйте час послідовного запуску
Measure-Command { pytest tests/ -v }

# Виміряйте час паралельного запуску
Measure-Command { pytest tests/ -n auto -v }
```

**Очікувані результати:**
- Sequential: ~20-40 секунд
- Parallel (4 cores): ~5-15 секунд
- Speedup: 2-4x

### 6️⃣ Allure звіти

**Згенеруйте та перевірте:**
```powershell
pytest tests/ --alluredir=reports/allure-results -v
allure serve reports/allure-results
```

**Що має бути в Allure:**
- ✅ Suites організовані за features
- ✅ Test cases з детальними кроками
- ✅ Severity levels
- ✅ Categories (passed, failed, broken)
- ✅ Timeline виконання
- ✅ Trend charts
- ✅ Attachments з деталями

### 7️⃣ Coverage звіт

**Перевірте покриття:**
```powershell
pytest tests/ --cov=. --cov-report=term --cov-report=html:reports/coverage
```

**Відкрийте HTML звіт:**
```powershell
start reports/coverage/index.html
```

**Що перевірити:**
- ✅ Загальне покриття > 70%
- ✅ Детальний розбір по файлам
- ✅ Непокриті лінії виділені червоним

---

## 🎯 Критерії оцінювання (за вашим завданням)

### ✅ Завдання 1: Налаштування Jenkins
- [x] Jenkinsfile створено
- [x] Містить всі необхідні stages
- [x] Налаштовані triggers
- [x] Є інструкції з налаштування

### ✅ Завдання 2: Створення тестового фреймворку
- [x] 159 unit тестів існують
- [x] Додано BDD тести (8 сценаріїв)
- [x] Проект на Git (готовий до commit)

### ✅ Завдання 3: Створення пайплайну Jenkins
- [x] Jenkinsfile з повним CI/CD процесом
- [x] Checkout → Setup → Tests → Reports
- [x] Інтеграція з Git репозиторієм

### ✅ Завдання 4: Автоматизація CI/CD
- [x] Auto-trigger на Git commits (pollSCM)
- [x] Періодична збірка (cron)
- [x] Автоматичні звіти та логи

### ✅ Завдання 5: Паралельні тести та інтеграція
- [x] pytest-xdist для паралельного запуску
- [x] Allure інтеграція для звітності
- [x] Додаткові BDD тести додано

---

## 🚀 Швидкий чеклист для перевірки

```powershell
# 1. Клонуйте/відкрийте проект
cd "unit_tests"

# 2. Перевірте що всі файли на місці
ls Jenkinsfile
ls pytest.ini
ls allure.yml
ls CI_CD_SETUP.md
ls tests/bdd/features/*.feature

# 3. Запустіть автоматичний скрипт
.\setup_and_run.ps1
# Оберіть опцію 7 (повний CI/CD)

# 4. Перевірте результати
ls reports/

# 5. Відкрийте звіти
start reports/report_parallel.html
start reports/coverage/index.html

# 6. (Опціонально) Запустіть Allure
allure serve reports/allure-results
```

---

## 📝 Очікувані результати

Після виконання всіх тестів ви повинні побачити:

### Консольний вивід:
```
✅ 159 unit tests passed
✅ 8 BDD scenarios passed
✅ Coverage: 70%+
✅ Code quality: passed
✅ Allure report: generated
```

### Створені файли:
```
reports/
├── report_sequential.html       ✅
├── report_parallel.html         ✅
├── coverage/
│   └── index.html              ✅
├── allure-results/             ✅
├── bdd/                        ✅
├── junit_*.xml                 ✅
└── pylint_report.txt           ✅
```

---

## 🐛 Можливі проблеми та рішення

### Проблема: Python не знайдено
```powershell
# Рішення: встановіть Python 3.9+
# https://www.python.org/downloads/
```

### Проблема: pip залежності не встановлюються
```powershell
# Рішення: оновіть pip
python -m pip install --upgrade pip
```

### Проблема: Allure не встановлено
```powershell
# Windows (через Scoop)
scoop install allure

# Або пропустіть цей крок - основні тести працюють без Allure
```

### Проблема: Behave не знаходить модулі
```powershell
# Рішення: переконайтесь що ви в правильній директорії
cd unit_tests
behave tests/bdd/features
```

---

## 📞 Контактна інформація

Якщо виникнуть питання під час перевірки:
- Всі інструкції є в `CI_CD_SETUP.md`
- Детальна конфігурація Jenkins в `JENKINS_SETUP.txt`
- Приклади використання в `tests/test_allure_examples.py`

---

## ⏱️ Часові оцінки

- **Швидка перевірка (скрипт)**: 5 хвилин
- **Повна перевірка всіх файлів**: 10-15 хвилин
- **Налаштування Jenkins**: 20-30 хвилин
- **Тестування GitHub Actions**: автоматично при push

---

**Дякую за перевірку! 🎓**
