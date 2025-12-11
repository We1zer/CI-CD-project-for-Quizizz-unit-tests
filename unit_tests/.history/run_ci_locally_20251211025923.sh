#!/bin/bash
# Local CI/CD Runner Script for Linux/macOS
# Імітує Jenkins pipeline локально

set -e  # Exit on error

echo "🚀 Starting Local CI/CD Pipeline..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Stage 1: Setup Environment
echo -e "\n${YELLOW}📦 Stage 1: Setting up Python environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}Virtual environment exists, activating...${NC}"
    source venv/bin/activate
else
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Stage 2: Linting
echo -e "\n${YELLOW}🔍 Stage 2: Running code linting...${NC}"
echo -e "${GREEN}Running flake8...${NC}"
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || {
    echo -e "${RED}⚠️ Critical linting errors found!${NC}"
}

flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
echo -e "${GREEN}✅ Linting completed${NC}"

# Stage 3: Run Tests (Parallel)
echo -e "\n${YELLOW}🧪 Stage 3: Running unit tests (parallel)...${NC}"
TEST_START=$(date +%s)
pytest tests/ -n auto --maxprocesses=4 \
    --alluredir=allure-results \
    --junitxml=reports/junit.xml \
    --html=reports/report.html \
    --self-contained-html \
    -v --tb=short
TEST_EXIT_CODE=$?
TEST_END=$(date +%s)
TEST_DURATION=$((TEST_END - TEST_START))

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed in ${TEST_DURATION} seconds${NC}"
else
    echo -e "${RED}❌ Some tests failed (exit code: ${TEST_EXIT_CODE})${NC}"
fi

# Stage 4: BDD Tests
echo -e "\n${YELLOW}🎭 Stage 4: Running BDD tests...${NC}"
pytest tests/bdd/ --alluredir=allure-results -v
BDD_EXIT_CODE=$?

if [ $BDD_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ BDD tests passed${NC}"
else
    echo -e "${YELLOW}⚠️ Some BDD tests failed (exit code: ${BDD_EXIT_CODE})${NC}"
fi

# Stage 5: Coverage Report
echo -e "\n${YELLOW}📊 Stage 5: Generating coverage report...${NC}"
pytest tests/ --cov=. --cov-report=html:reports/coverage \
    --cov-report=xml:reports/coverage.xml \
    --cov-report=term

# Stage 6: Allure Report
echo -e "\n${YELLOW}📈 Stage 6: Generating Allure report...${NC}"
if command -v allure &> /dev/null; then
    allure generate allure-results -o allure-report --clean
    echo -e "${GREEN}✅ Allure report generated${NC}"
    echo -e "${CYAN}To view report, run: allure open allure-report${NC}"
else
    echo -e "${YELLOW}⚠️ Allure not installed. Skipping report generation.${NC}"
    echo -e "${CYAN}Install: sudo apt install allure${NC}"
fi

# Summary
echo -e "\n${CYAN}============================================================${NC}"
echo -e "${CYAN}📋 CI/CD Pipeline Summary${NC}"
echo -e "${CYAN}============================================================${NC}"
echo -e "Duration: ${TEST_DURATION} seconds"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "Unit Tests: ${GREEN}✅ PASSED${NC}"
else
    echo -e "Unit Tests: ${RED}❌ FAILED${NC}"
fi

if [ $BDD_EXIT_CODE -eq 0 ]; then
    echo -e "BDD Tests: ${GREEN}✅ PASSED${NC}"
else
    echo -e "BDD Tests: ${YELLOW}⚠️ WARNING${NC}"
fi

echo ""
echo -e "Reports available at:"
echo -e "  ${CYAN}- HTML: reports/report.html${NC}"
echo -e "  ${CYAN}- Coverage: reports/coverage/index.html${NC}"
echo -e "  ${CYAN}- Allure: allure-report/index.html${NC}"
echo -e "${CYAN}============================================================${NC}"

# Exit with appropriate code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✅ Pipeline completed successfully!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Pipeline failed!${NC}"
    exit 1
fi
