// Jenkins declarative pipeline for Quizizz test automation
//
// This Jenkinsfile defines a simple CI/CD pipeline for building and testing
// the Quizizz test framework written in .NET Core.  It demonstrates how to
// restore NuGet packages, compile the solution, execute unit and BDD tests,
// generate test reports and publish Allure results.  Adjust the stages and
// tooling paths according to your environment.

pipeline {
    agent any

    // Define global tools.  These names must match the tool installations
    // configured in Jenkins (Manage Jenkins → Global Tool Configuration).
    tools {
        // Name of the .NET SDK installation as configured in Jenkins
        // For example, if you configured a .NET installation named "dotnet-8.0", use that here.
        dotnet "dotnet"
    }

    // Trigger builds on every commit and periodically every night at 02:00
    triggers {
        pollSCM('H/5 * * * *')
        cron('H 2 * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout from the SCM specified when creating the pipeline job
                checkout scm
            }
        }

        stage('Restore') {
            steps {
                // Restore NuGet packages for all projects in the solution
                // The --locked-mode option ensures restore fails if the lock file is outdated
                sh 'dotnet restore --locked-mode'
            }
        }

        stage('Build') {
            steps {
                // Build solution in Release configuration
                sh 'dotnet build --configuration Release --no-restore'
            }
        }

        stage('Test') {
            steps {
                // Ensure the TestResults directory exists
                sh 'mkdir -p TestResults'

                // Run tests and output a .trx file for each test project
                // The --no-build flag reuses the build artifacts from the previous stage
                sh 'dotnet test tests/Quizizz.Tests/Quizizz.Tests.csproj --no-build --no-restore --configuration Release \
                     --logger "trx;LogFileName=quizizz_tests.trx" \
                     --results-directory TestResults'

                // Convert the .trx results into Allure format
                // Requires the Allure CLI installed on the Jenkins agent and configured in PATH
                sh 'allure generate --clean TestResults --output TestResults/allure-report || true'
            }

            post {
                always {
                    // Publish test results to Jenkins.  If you install the
                    // JUnit plugin, Jenkins can display these results.
                    junit allowEmptyResults: true, testResults: 'TestResults/*.trx'

                    // Publish Allure results (requires Allure Jenkins plugin)
                    allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'TestResults/allure-report']]
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                // Example deployment stage.  Replace this with real deployment
                // commands, e.g. copying artifacts to a server or publishing
                // results.  This stage runs only on the main branch.
                sh 'echo "Deploying application..."'
            }
        }
    }

    post {
        failure {
            // Send a notification or take other actions on failure
            echo 'Build failed!'
        }
        success {
            echo 'Build succeeded!'
        }
    }
}