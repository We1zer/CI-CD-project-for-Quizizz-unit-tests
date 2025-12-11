# CI/CD Налаштування для Quizizz Unit Tests

## 📚 Зміст

- [Огляд](#огляд)
- [Встановлення Jenkins](#встановлення-jenkins)
- [Налаштування Jenkins](#налаштування-jenkins)
- [Запуск тестів локально](#запуск-тестів-локально)
- [GitHub Actions](#github-actions)
- [Allure Reports](#allure-reports)
- [Паралельне виконання тестів](#паралельне-виконання-тестів)
- [BDD тести](#bdd-тести)

---

## 🎯 Огляд

Цей проект містить повну CI/CD інфраструктуру для тестування Quizizz фреймворку з:
- ✅ Jenkins Pipeline (Jenkinsfile)
- ✅ GitHub Actions workflow
- ✅ Паралельне виконання тестів (pytest-xdist)
- ✅ Allure звітність
- ✅ BDD тести (Behave)
- ✅ Покриття коду (Coverage)

---

## 🔧 Встановлення Jenkins

### Windows

1. **Завантажте Jenkins**
   ```powershell
   # Завантажте Jenkins MSI з офіційного сайту
   # https://www.jenkins.io/download/
   ```

2. **Встановіть Jenkins**
   - Запустіть інсталятор
   - Оберіть порт (за замовчуванням 8080)
   - Дочекайтесь завершення інсталяції

3. **Перший запуск**
   - Відкрийте браузер: `http://localhost:8080`
   - Знайдіть пароль адміністратора:
   ```powershell
   Get-Content "C:\Program Files\Jenkins\secrets\initialAdminPassword"
   ```

### Linux / macOS

```bash
# Для Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

# Запуск Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

---

## ⚙️ Налаштування Jenkins

### 1. Встановлення плагінів

У Jenkins Dashboard перейдіть до: **Manage Jenkins** → **Manage Plugins** → **Available**

Встановіть наступні плагіни:
- ✅ **Git Plugin** - для роботи з Git репозиторіями
- ✅ **Pipeline** - для Pipeline jobs
- ✅ **HTML Publisher** - для публікації HTML звітів
- ✅ **Allure Jenkins Plugin** - для Allure звітів
- ✅ **JUnit Plugin** - для публікації JUnit результатів
- ✅ **Cobertura Plugin** - для покриття коду

### 2. Налаштування Global Tools

**Manage Jenkins** → **Global Tool Configuration**

#### Python
```
Name: Python 3.9
Install automatically: ✓
Version: Python 3.9.x
```

#### Allure
```
Name: Allure
Install automatically: ✓
Version: 2.24.0
```

### 3. Створення Jenkins Pipeline Job

1. **Натисніть "New Item"**
2. **Введіть назву**: `Quizizz-Unit-Tests`
3. **Оберіть**: `Pipeline`
4. **Натисніть**: `OK`

#### Конфігурація Pipeline

**Pipeline Definition**:
- Definition: `Pipeline script from SCM`
- SCM: `Git`
- Repository URL: `https://github.com/ваш-username/quizizz-ci-cd.git`
- Script Path: `unit_tests/Jenkinsfile`

**Build Triggers** (виберіть потрібні):
- ✅ Poll SCM: `H/5 * * * *` (кожні 5 хвилин)
- ✅ Build periodically: `0 2 * * *` (щодня о 2:00)

---

## 🚀 Запуск тестів локально

### Встановлення залежностей

```powershell
cd unit_tests
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Запуск всіх тестів

```powershell
# Звичайний запуск
pytest tests/ -v

# З HTML звітом
pytest tests/ -v --html=reports/report.html --self-contained-html

# Паралельний запуск
pytest tests/ -n auto -v

# З покриттям коду
pytest tests/ --cov=. --cov-report=html:reports/coverage
```

### Запуск конкретних тестів

```powershell
# Один тестовий файл
pytest tests/test_quiz_search.py -v

# Один тест
pytest tests/test_quiz_search.py::test_basic_search -v

# Тести з маркером
pytest tests/ -m smoke -v
```

### Запуск BDD тестів

```powershell
cd unit_tests
behave tests/bdd/features -v
```

---

## 🌐 GitHub Actions

### Автоматичний запуск

GitHub Actions автоматично запускається при:
- 📤 Push до гілок `main` або `develop`
- 🔀 Pull Request до цих гілок
- 🕐 Щоденно о 2:00 UTC
- 🖱️ Ручний запуск через UI

### Перегляд результатів

1. Відкрийте ваш репозиторій на GitHub
2. Перейдіть до вкладки **Actions**
3. Оберіть потрібний workflow run
4. Переглядайте логи та артефакти

### Allure Report на GitHub Pages

Після успішного запуску:
- Звіт публікується на: `https://ваш-username.github.io/quizizz-ci-cd/`

---

## 📊 Allure Reports

### Локальна генерація

```powershell
# Запустіть тести з Allure
pytest tests/ --alluredir=reports/allure-results -v

# Згенеруйте звіт
allure serve reports/allure-results
```

### Встановлення Allure (якщо потрібно)

**Windows** (через Scoop):
```powershell
scoop install allure
```

**macOS**:
```bash
brew install allure
```

**Linux**:
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

---

## ⚡ Паралельне виконання тестів

### pytest-xdist (рекомендовано)

```powershell
# Автоматичне визначення кількості процесів
pytest tests/ -n auto

# Конкретна кількість процесів
pytest tests/ -n 4

# З розподілом за файлами
pytest tests/ -n auto --dist loadfile
```

### pytest-parallel

```powershell
# Паралельні workers
pytest tests/ --workers 4

# Паралельні тести в межах класу
pytest tests/ --tests-per-worker auto
```

### Порівняння продуктивності

Jenkinsfile включає обидва методи для порівняння:
- **Sequential**: звичайний послідовний запуск
- **Parallel**: паралельний з pytest-xdist

---

## 🥒 BDD тести

### Структура

```
unit_tests/tests/bdd/
├── features/
│   ├── quiz_search.feature      # Сценарії пошуку
│   └── quiz_library.feature     # Сценарії бібліотеки
├── steps/
│   └── quiz_steps.py            # Імплементація кроків
└── environment.py               # Конфігурація Behave
```

### Запуск BDD тестів

```powershell
# Всі BDD тести
behave tests/bdd/features

# З тегами
behave tests/bdd/features --tags=@smoke

# З форматованим виводом
behave tests/bdd/features --format pretty

# З JUnit звітом
behave tests/bdd/features --junit --junit-directory reports/bdd
```

### Приклад feature файлу

```gherkin
# language: uk
Функціонал: Пошук квізів

  Сценарій: Успішний пошук
    Дано я відкрив сторінку пошуку
    Коли я введу "Python" в поле пошуку
    Тоді я побачу список квізів з результатами
```

---

## 📈 Метрики та звітність

### Coverage Report

```powershell
# Генерація HTML звіту
pytest tests/ --cov=. --cov-report=html:reports/coverage

# Перегляд звіту
start reports/coverage/index.html
```

### Pytest HTML Report

```powershell
pytest tests/ --html=reports/report.html --self-contained-html
start reports/report.html
```

---

## 🔍 Перевірка коду

### Pylint

```powershell
pylint *.py --output-format=text --reports=y
```

### Flake8

```powershell
flake8 . --count --statistics
```

---

## 🐛 Troubleshooting

### Jenkins не бачить Python

```powershell
# Додайте Python до PATH в Jenkins
# Manage Jenkins → Configure System → Environment variables
# KEY: PATH
# VALUE: C:\Python39;C:\Python39\Scripts;%PATH%
```

### Allure плагін не працює

```
1. Перевірте встановлення: Manage Jenkins → Global Tool Configuration → Allure Commandline
2. Переконайтесь що плагін встановлено: Manage Plugins → Installed → Allure Jenkins Plugin
3. Перезапустіть Jenkins
```

### Тести падають на Windows

```powershell
# Переконайтесь що використовуєте правильні слеші
# У Jenkinsfile для Windows використовуйте bat замість sh
```

---

## 📞 Контакти та підтримка

Для питань створюйте Issue в репозиторії проекту.

---

## 📝 Чеклист налаштування

- [ ] Jenkins встановлено та запущено
- [ ] Плагіни встановлено (Git, Pipeline, Allure, HTML Publisher)
- [ ] Global Tools налаштовано (Python, Allure)
- [ ] Pipeline Job створено
- [ ] Git репозиторій підключено
- [ ] Build triggers налаштовано
- [ ] Тести запускаються локально
- [ ] GitHub Actions workflow працює
- [ ] Allure звіти генеруються
- [ ] BDD тести виконуються

---

**Успіхів з автоматизацією! 🚀**
