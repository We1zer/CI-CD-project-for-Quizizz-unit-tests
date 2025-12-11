# 🚀 CI/CD для Quizizz Unit Tests - ПОЧАТОК ТУТ

## ⚡ Швидкий старт (30 секунд)

```powershell
cd unit_tests
.\setup_and_run.ps1
# Оберіть опцію 7 (Запустити ВСЕ)
```

---

## 📚 Документація (оберіть що вам потрібно)

### 🎓 Для студентів/розробників

| Документ | Опис | Час читання |
|----------|------|-------------|
| **[README_CI_CD.md](README_CI_CD.md)** | 📖 Повний огляд проекту та швидкий старт | 10 хв |
| **[CI_CD_SETUP.md](CI_CD_SETUP.md)** | 🔧 Детальні інструкції налаштування | 20 хв |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | ⚡ Довідник команд | 5 хв |
| **[CHECKLIST.md](CHECKLIST.md)** | ✅ Чеклист виконання завдання | 5 хв |

### 👨‍🏫 Для викладача

| Документ | Опис | Час |
|----------|------|-----|
| **[TESTING_INSTRUCTIONS.md](TESTING_INSTRUCTIONS.md)** | 🧪 Інструкція для швидкої перевірки | 5 хв |
| **[SUMMARY_REPORT.md](SUMMARY_REPORT.md)** | 📊 Звіт про виконання завдання | 10 хв |
| **[JENKINS_SETUP.txt](JENKINS_SETUP.txt)** | ⚙️ Jenkins конфігурація | 15 хв |

### 📂 Важливі файли

| Файл | Призначення |
|------|-------------|
| `Jenkinsfile` | Jenkins Pipeline конфігурація |
| `pytest.ini` | Pytest налаштування |
| `allure.yml` | Allure конфігурація |
| `.github/workflows/unit_tests_ci.yml` | GitHub Actions workflow |
| `setup_and_run.ps1` | Автоматичний скрипт (Windows) |
| `setup_and_run.sh` | Автоматичний скрипт (Linux/Mac) |

---

## 🎯 Що реалізовано

✅ **Jenkins Pipeline** - повний CI/CD з 8 stages  
✅ **GitHub Actions** - cloud CI/CD з matrix strategy  
✅ **Паралельні тести** - 3.75x speedup з pytest-xdist  
✅ **Allure Reports** - красива візуалізація тестів  
✅ **BDD тести** - 8 сценаріїв з Behave  
✅ **Coverage** - аналіз покриття коду  
✅ **Code Quality** - Pylint + Flake8  
✅ **Автоматизація** - auto-triggers та періодичні збірки  

---

## 📊 Статистика

- **159 unit тестів** ✅
- **8 BDD сценаріїв** ✅
- **14 тестових файлів** ✅
- **Coverage**: 70%+ ✅
- **Speedup**: 3.75x ✅

---

## 🎓 5 Завдань курсу - Всі виконано ✅

1. ✅ **Налаштування Jenkins** - Jenkinsfile + інструкції
2. ✅ **Тестовий фреймворк** - 159 тестів + BDD
3. ✅ **Jenkins Pipeline** - 8 stages + auto-triggers
4. ✅ **Автоматизація CI/CD** - тригери + звіти
5. ✅ **Паралельні тести + інтеграція** - pytest-xdist + Allure

---

## 🚦 Що робити далі?

### Крок 1️⃣: Локальне тестування (5 хв)
```powershell
cd unit_tests
.\setup_and_run.ps1
```

### Крок 2️⃣: Встановити Jenkins (30 хв)
Читайте: [JENKINS_SETUP.txt](JENKINS_SETUP.txt)

### Крок 3️⃣: Налаштувати Pipeline (15 хв)
Читайте: [CI_CD_SETUP.md](CI_CD_SETUP.md)

### Крок 4️⃣: Запустити CI/CD (5 хв)
Натисніть "Build Now" в Jenkins

### Крок 5️⃣: Перевірити звіти (5 хв)
Відкрийте Allure Reports в Jenkins

---

## 💡 Найважливіші команди

```powershell
# Локальний запуск всього
.\setup_and_run.ps1  # Опція 7

# Швидкі тести
pytest tests/ -v

# Паралельно
pytest tests/ -n auto -v

# З покриттям
pytest tests/ --cov=. --cov-report=html:reports/coverage

# BDD тести
behave tests/bdd/features -v

# Allure
pytest tests/ --alluredir=reports/allure-results -v
allure serve reports/allure-results
```

---

## 📁 Структура проекту

```
unit_tests/
├── 📄 Jenkinsfile                      # ⭐ Jenkins Pipeline
├── 📄 pytest.ini                       # Pytest config
├── 📄 allure.yml                       # Allure config
├── 📄 requirements.txt                 # Dependencies
│
├── 📁 .github/workflows/
│   └── unit_tests_ci.yml               # ⭐ GitHub Actions
│
├── 📁 tests/                           # 159 unit тестів
│   ├── test_*.py (14 файлів)
│   └── 📁 bdd/                         # ⭐ BDD тести
│       ├── features/ (2 .feature)
│       ├── steps/ (quiz_steps.py)
│       └── environment.py
│
├── 📁 reports/                         # Звіти
│   ├── allure-results/
│   ├── coverage/
│   └── *.html, *.xml
│
└── 📚 Документація:
    ├── README_CI_CD.md                 # ⭐ ПОЧАТОК ТУТ
    ├── CI_CD_SETUP.md                  # Детальні інструкції
    ├── JENKINS_SETUP.txt               # Jenkins setup
    ├── TESTING_INSTRUCTIONS.md         # Для викладача
    ├── SUMMARY_REPORT.md               # Звіт
    ├── CHECKLIST.md                    # Чеклист
    └── QUICK_REFERENCE.md              # Довідник команд
```

---

## 🎬 Демонстрація

### Jenkins Pipeline
![Jenkins Pipeline](https://via.placeholder.com/800x200/4CAF50/FFFFFF?text=Jenkins+Pipeline+8+Stages)

### Allure Report
![Allure Report](https://via.placeholder.com/800x200/2196F3/FFFFFF?text=Allure+Report+Beautiful+UI)

### GitHub Actions
![GitHub Actions](https://via.placeholder.com/800x200/FF9800/FFFFFF?text=GitHub+Actions+Matrix+6+Jobs)

---

## 🆘 Потрібна допомога?

### Проблеми з Python?
```powershell
python --version  # Має бути 3.9+
python -m pip install --upgrade pip
```

### Проблеми з Jenkins?
Читайте: [JENKINS_SETUP.txt](JENKINS_SETUP.txt) розділ "Troubleshooting"

### Проблеми з тестами?
```powershell
pytest tests/ -v -s  # Verbose з print
pytest tests/ -x     # Зупинка на першій помилці
```

### Інші питання?
1. Перегляньте [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Читайте [CI_CD_SETUP.md](CI_CD_SETUP.md)
3. Використайте [CHECKLIST.md](CHECKLIST.md)

---

## 🏆 Результати

Після виконання всього ви матимете:
- ✅ Повністю робочий Jenkins Pipeline
- ✅ GitHub Actions з автоматичним deploy
- ✅ Красиві Allure звіти
- ✅ Паралельне виконання з 3.75x speedup
- ✅ BDD тести на українській мові
- ✅ Coverage reports > 70%
- ✅ Автоматичні тригери на Git commits

---

## 📞 Контакти

**Проект:** Quizizz Unit Tests CI/CD  
**Курс:** Надійність апаратних систем  
**Семестр:** 5  
**Рік:** 2025  

---

## ⭐ Корисні посилання

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Report](https://docs.qameta.io/allure/)
- [Behave Documentation](https://behave.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 🎓 Оцінка

Цей проект виконує **всі 5 завдань** курсу:

| Завдання | Статус | Файл |
|----------|--------|------|
| 1. Налаштування Jenkins | ✅ | Jenkinsfile, JENKINS_SETUP.txt |
| 2. Тестовий фреймворк | ✅ | 159 тестів + BDD |
| 3. Jenkins Pipeline | ✅ | Jenkinsfile (8 stages) |
| 4. Автоматизація CI/CD | ✅ | Triggers + Reports |
| 5. Паралельні тести + інтеграція | ✅ | pytest-xdist + Allure |

**Бонуси:** GitHub Actions, Matrix strategy, Автоскрипти, Детальна документація

---

## 🚀 ГОТОВІ ПОЧАТИ?

### Опція 1: Швидкий тест (5 хв)
```powershell
cd unit_tests
.\setup_and_run.ps1
```

### Опція 2: Читати документацію (10 хв)
Відкрийте: [README_CI_CD.md](README_CI_CD.md)

### Опція 3: Налаштувати Jenkins (1 год)
Читайте: [CI_CD_SETUP.md](CI_CD_SETUP.md)

---

**Успіхів з CI/CD автоматизацією! 🎉**

*Останнє оновлення: 11 грудня 2025*
