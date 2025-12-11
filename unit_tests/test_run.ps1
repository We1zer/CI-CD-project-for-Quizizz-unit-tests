Write-Host 'CI/CD Test Script' -ForegroundColor Cyan
Write-Host 'Running pytest tests...' -ForegroundColor Yellow
pytest tests/ -v
