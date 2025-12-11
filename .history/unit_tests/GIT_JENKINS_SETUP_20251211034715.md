# 🔧 ІНСТРУКЦІЯ: Налаштування автоматичного запуску Jenkins на Git commit

## ✅ ЩО ВЖЕ ГОТОВО:

Ваш `Jenkinsfile` вже містить налаштування для автоматичного запуску:

```groovy
triggers {
    // Автоматичний запуск при зміні в Git (перевірка кожні 5 хвилин)
    pollSCM('H/5 * * * *')
    
    // Періодична збірка кожен день о 2:00
    cron('0 2 * * *')
}
```

## 📝 КРОК 1: Ініціалізація Git репозиторію

### Варіант A: Локальний Git (для тестування)

```powershell
# 1. Перейдіть в директорію unit_tests
cd "C:\Users\taras\Desktop\5sem\Надійність апаратних систем\quizizz-ci-cd\unit_tests"

# 2. Ініціалізуйте Git
git init

# 3. Додайте всі файли
git add .

# 4. Зробіть перший commit
git commit -m "Initial commit: CI/CD setup with Jenkins, BDD tests, and Allure"

# 5. Перевірте статус
git status
git log --oneline
```

### Варіант B: GitHub репозиторій (рекомендовано)

```powershell
# 1. Створіть репозиторій на GitHub
# Відкрийте: https://github.com/new
# Назва: quizizz-ci-cd
# Опис: CI/CD project for Quizizz unit tests
# Public або Private - на ваш вибір

# 2. Ініціалізуйте Git локально
cd "C:\Users\taras\Desktop\5sem\Надійність апаратних систем\quizizz-ci-cd"
git init

# 3. Додайте remote
git remote add origin https://github.com/ВАШ-USERNAME/quizizz-ci-cd.git

# 4. Додайте файли
git add .

# 5. Commit
git commit -m "Initial commit: CI/CD setup with Jenkins, BDD tests, and Allure"

# 6. Push до GitHub
git branch -M main
git push -u origin main
```

---

## 📝 КРОК 2: Налаштування Jenkins для Git

### Спосіб 1: SCM Polling (простіше, вже налаштовано)

Jenkins буде **автоматично перевіряти** Git репозиторій кожні 5 хвилин:

1. **Відкрийте Jenkins**: http://localhost:8080
2. **Створіть новий Pipeline Job**:
   - Натисніть "New Item"
   - Введіть назву: `Quizizz-Unit-Tests-CI`
   - Виберіть: "Pipeline"
   - Натисніть "OK"

3. **Налаштуйте Pipeline**:
   - **General**:
     - ☑ Discard old builds
     - Max # of builds to keep: 10
   
   - **Build Triggers**:
     - ☑ Poll SCM
     - Schedule: `H/5 * * * *` (кожні 5 хвилин)
   
   - **Pipeline**:
     - Definition: "Pipeline script from SCM"
     - SCM: "Git"
     - Repository URL: 
       - Локально: `file:///C:/Users/taras/Desktop/5sem/Надійність апаратних систем/quizizz-ci-cd`
       - GitHub: `https://github.com/ВАШ-USERNAME/quizizz-ci-cd.git`
     - Branch: `*/main` (або `*/master`)
     - Script Path: `unit_tests/Jenkinsfile`

4. **Збережіть конфігурацію**

### Спосіб 2: GitHub Webhooks (найкращий для GitHub)

Якщо ви використовуєте GitHub, налаштуйте webhook для **миттєвого** запуску:

1. **У Jenkins**:
   - Встановіть плагін "GitHub Integration Plugin"
   - У Job конфігурації:
     - Build Triggers → ☑ GitHub hook trigger for GITScm polling

2. **На GitHub**:
   - Відкрийте ваш репозиторій
   - Settings → Webhooks → Add webhook
   - Payload URL: `http://YOUR-JENKINS-URL:8080/github-webhook/`
   - Content type: `application/json`
   - Events: ☑ Just the push event
   - ☑ Active
   - Add webhook

**Примітка**: Для локального Jenkins потрібен публічний URL (використайте ngrok):

```powershell
# Встановіть ngrok: https://ngrok.com/
ngrok http 8080

# Використайте URL з ngrok у GitHub webhook
# Наприклад: https://abc123.ngrok.io/github-webhook/
```

---

## 📝 КРОК 3: Тестування автоматичного запуску

### Тест 1: Перевірка SCM Polling

```powershell
# 1. Зробіть зміну у файлі
cd "C:\Users\taras\Desktop\5sem\Надійність апаратних систем\quizizz-ci-cd"
echo "# Test change" >> README.md

# 2. Commit та push
git add README.md
git commit -m "Test: trigger Jenkins build"
git push

# 3. Почекайте до 5 хвилин
# Jenkins перевірить Git та запустить збірку автоматично

# 4. Перевірте в Jenkins
# Відкрийте: http://localhost:8080/job/Quizizz-Unit-Tests-CI/
# Має з'явитися новий build
```

### Тест 2: Ручний запуск (для перевірки)

1. Відкрийте Jenkins job
2. Натисніть "Build Now"
3. Подивіться Console Output

---

## 📝 КРОК 4: Налаштування періодичної збірки

**Вже налаштовано** в Jenkinsfile:

```groovy
cron('0 2 * * *')  // Щодня о 2:00
```

### Інші варіанти розкладу:

```groovy
// Кожні 15 хвилин
cron('H/15 * * * *')

// Кожну годину
cron('H * * * *')

// Щодня о 8:00, 12:00, 18:00
cron('0 8,12,18 * * *')

// Тільки в робочі дні о 9:00
cron('0 9 * * 1-5')

// Щосуботи о 0:00
cron('0 0 * * 6')
```

Щоб змінити розклад, відредагуйте `unit_tests/Jenkinsfile`, рядок з `cron()`.

---

## 📝 КРОК 5: Додаткові обмеження CI/CD

### У Jenkins Job Configuration додайте:

1. **Build Environment**:
   - ☑ Abort the build if it's stuck
   - Timeout: 30 minutes
   - Timeout strategy: Absolute

2. **Post-build Actions** (додайте до Jenkinsfile):

```groovy
post {
    always {
        // Очищення workspace після збірки
        cleanWs()
    }
    
    success {
        // Email нотифікація при успіху
        emailext (
            subject: "✅ Build Successful: ${currentBuild.fullDisplayName}",
            body: "Build succeeded! Check: ${env.BUILD_URL}",
            to: "your-email@example.com"
        )
    }
    
    failure {
        // Email нотифікація при помилці
        emailext (
            subject: "❌ Build Failed: ${currentBuild.fullDisplayName}",
            body: "Build failed! Check: ${env.BUILD_URL}",
            to: "your-email@example.com"
        )
    }
}
```

---

## 📝 КРОК 6: Перевірка правильності роботи

### Чеклист перевірки:

- [ ] **Git репозиторій створено**
  ```powershell
  git remote -v
  git log --oneline
  ```

- [ ] **Jenkins Job створено**
  - Відкрийте: http://localhost:8080

- [ ] **SCM Polling працює**
  - Jenkins → Job → Poll Log (має показувати перевірки)

- [ ] **Ручний build успішний**
  - Натисніть "Build Now"
  - Перевірте Console Output
  - Всі stages мають бути зелені

- [ ] **Автоматичний build після commit**
  - Зробіть commit
  - Почекайте 5 хвилин
  - Перевірте чи з'явився новий build

- [ ] **Звіти генеруються**
  - HTML Reports
  - Allure Reports
  - JUnit XML
  - Coverage Reports

- [ ] **Періодична збірка налаштована**
  - Перевірте cron у Jenkinsfile
  - Перевірте у Jenkins Job → Configure → Build Triggers

---

## 🎯 ШВИДКИЙ ТЕСТ (5 хвилин)

```powershell
# 1. Ініціалізація Git
cd "C:\Users\taras\Desktop\5sem\Надійність апаратних систем\quizizz-ci-cd"
git init
git add .
git commit -m "Initial commit: CI/CD setup"

# 2. Створіть Jenkins Job з налаштуваннями вище

# 3. Запустіть вручну
# Jenkins → Job → Build Now

# 4. Зробіть тестовий commit
echo "# Test" >> unit_tests/README.md
git add unit_tests/README.md
git commit -m "Test: auto-trigger"

# 5. Почекайте 5 хвилин та перевірте Jenkins
```

---

## 📊 Очікувані результати:

✅ **При кожному commit**:
- Jenkins автоматично виявляє зміни (до 5 хв)
- Запускає Pipeline
- Виконує всі stages
- Генерує звіти
- Зберігає artifacts

✅ **Щодня о 2:00**:
- Автоматичний запуск збірки
- Regression testing

✅ **При помилці**:
- Build стає червоним
- Email нотифікація (якщо налаштовано)
- Логи зберігаються

---

## 🔧 Troubleshooting

### Jenkins не бачить Git зміни:
```powershell
# Перевірте Poll Log
Jenkins → Job → Poll Log

# Має показувати щось типу:
# "Changes found"
```

### Build не запускається автоматично:
1. Перевірте Build Triggers в Job Configuration
2. Перевірте правильність Git URL
3. Перевірте Poll Log для помилок

### Git credentials проблеми:
```powershell
# Для HTTPS репозиторію
Jenkins → Manage Jenkins → Manage Credentials
# Додайте GitHub username + Personal Access Token
```

---

## ✅ ФІНАЛЬНИЙ ЧЕКЛИСТ

- [ ] Git репозиторій ініціалізовано
- [ ] Всі файли додано до Git
- [ ] Jenkins Job створено
- [ ] SCM Polling налаштовано (H/5 * * * *)
- [ ] Періодична збірка налаштована (0 2 * * *)
- [ ] Ручний build пройшов успішно
- [ ] Автоматичний build спрацював після commit
- [ ] Звіти генеруються коректно

---

**Готово! Ваш CI/CD повністю автоматизований! 🚀**
