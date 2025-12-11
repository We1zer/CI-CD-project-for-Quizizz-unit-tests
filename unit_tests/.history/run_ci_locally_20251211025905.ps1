# Local CI/CD Runner Script
# Імітує Jenkins pipeline локально

Write-Host "🚀 Starting Local CI/CD Pipeline..." -ForegroundColor Cyan

# Stage 1: Setup Environment
Write-Host "`n📦 Stage 1: Setting up Python environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment exists, activating..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    Write-Host "Installing dependencies..." -ForegroundColor Green
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Stage 2: Linting
Write-Host "`n🔍 Stage 2: Running code linting..." -ForegroundColor Yellow
Write-Host "Running flake8..." -ForegroundColor Green
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Critical linting errors found!" -ForegroundColor Red
} else {
    Write-Host "✅ Critical checks passed" -ForegroundColor Green
}

flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Stage 3: Run Tests (Parallel)
Write-Host "`n🧪 Stage 3: Running unit tests (parallel)..." -ForegroundColor Yellow
$testStart = Get-Date
pytest tests/ -n auto --maxprocesses=4 `
    --alluredir=allure-results `
    --junitxml=reports/junit.xml `
    --html=reports/report.html `
    --self-contained-html `
    -v --tb=short

$testExitCode = $LASTEXITCODE
$testEnd = Get-Date
$testDuration = ($testEnd - $testStart).TotalSeconds

if ($testExitCode -eq 0) {
    Write-Host "✅ All tests passed in $testDuration seconds" -ForegroundColor Green
} else {
    Write-Host "❌ Some tests failed (exit code: $testExitCode)" -ForegroundColor Red
}

# Stage 4: BDD Tests
Write-Host "`n🎭 Stage 4: Running BDD tests..." -ForegroundColor Yellow
pytest tests/bdd/ --alluredir=allure-results -v
$bddExitCode = $LASTEXITCODE

if ($bddExitCode -eq 0) {
    Write-Host "✅ BDD tests passed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some BDD tests failed (exit code: $bddExitCode)" -ForegroundColor Yellow
}

# Stage 5: Coverage Report
Write-Host "`n📊 Stage 5: Generating coverage report..." -ForegroundColor Yellow
pytest tests/ --cov=. --cov-report=html:reports/coverage `
    --cov-report=xml:reports/coverage.xml `
    --cov-report=term

# Stage 6: Allure Report
Write-Host "`n📈 Stage 6: Generating Allure report..." -ForegroundColor Yellow
if (Get-Command allure -ErrorAction SilentlyContinue) {
    allure generate allure-results -o allure-report --clean
    Write-Host "✅ Allure report generated" -ForegroundColor Green
    Write-Host "To view report, run: allure open allure-report" -ForegroundColor Cyan
} else {
    Write-Host "⚠️ Allure not installed. Skipping report generation." -ForegroundColor Yellow
    Write-Host "Install: scoop install allure" -ForegroundColor Cyan
}

# Summary
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "📋 CI/CD Pipeline Summary" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "Duration: $testDuration seconds" -ForegroundColor White
Write-Host "Unit Tests: $(if ($testExitCode -eq 0) {'✅ PASSED'} else {'❌ FAILED'})" -ForegroundColor $(if ($testExitCode -eq 0) {'Green'} else {'Red'})
Write-Host "BDD Tests: $(if ($bddExitCode -eq 0) {'✅ PASSED'} else {'⚠️ WARNING'})" -ForegroundColor $(if ($bddExitCode -eq 0) {'Green'} else {'Yellow'})
Write-Host ""
Write-Host "Reports available at:" -ForegroundColor White
Write-Host "  - HTML: reports/report.html" -ForegroundColor Cyan
Write-Host "  - Coverage: reports/coverage/index.html" -ForegroundColor Cyan
Write-Host "  - Allure: allure-report/index.html" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

# Exit with appropriate code
if ($testExitCode -eq 0) {
    Write-Host "`n✅ Pipeline completed successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n❌ Pipeline failed!" -ForegroundColor Red
    exit 1
}
