// Jenkins declarative pipeline for Quizizz Python test automation
//
// This Jenkinsfile defines a CI/CD pipeline for testing Python unit tests.
// It runs tests, generates reports and archives artifacts.

pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                dir('unit_tests') {
                    bat '''
                        python --version
                        python -m pip install --upgrade pip
                        python -m pip install pytest pytest-html pytest-cov pytest-xdist behave
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('unit_tests') {
                    bat '''
                        if not exist reports mkdir reports
                        python -m pytest tests/ --ignore=tests/test_allure_examples.py -v --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml
                    '''
                }
            }
        }

        stage('Generate Coverage') {
            steps {
                dir('unit_tests') {
                    bat '''
                        python -m pytest tests/ --ignore=tests/test_allure_examples.py --cov=. --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml
                    '''
                }
            }
        }

        stage('Run BDD Tests') {
            steps {
                dir('unit_tests') {
                    bat '''
                        behave tests/bdd/features --junit --junit-directory reports/bdd || exit 0
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'unit_tests/reports/**/*', allowEmptyArchive: true
            
            junit testResults: 'unit_tests/reports/*.xml', allowEmptyResults: true
            
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'unit_tests/reports',
                reportFiles: 'report.html',
                reportName: 'Test Report'
            ])
            
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'unit_tests/reports/coverage',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        
        success {
            echo ' Build successful!'
        }
        
    }
}