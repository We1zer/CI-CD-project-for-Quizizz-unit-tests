# Quizizz CI/CD Test Framework Project

This repository contains a sample project illustrating how to set up a test
automation framework for the **Quizizz** platform along with a complete CI/CD
pipeline for Jenkins.  It is designed to satisfy the requirements outlined in
your assignment:

- Install and configure Jenkins on your local or virtual machine with the
  necessary plugins (Git, NuGet, MSBuild and the .NET Core SDK).  A modern
  version of Jenkins (LTS 2.440.x or newer) is recommended.
- Create a test framework and add code and assets to a version‑controlled
  project.
- Store the project in a Git repository.
- Create a Jenkins Pipeline job that checks out the repository, restores
  dependencies, builds the code and executes the tests.  The pipeline should
  support CI/CD best practices such as running automatically on every
  commit, scheduled builds and proper error handling.
- Support parallel test execution and integrate with a reporting tool such as
  **Allure** for rich test reports.
- Add Behaviour Driven Development (BDD) tests to verify new features in the
  framework.

The provided files offer a working starting point.  You can extend and
customise them to meet the full scope of your Quizizz automation goals.

## Repository structure

```
quizizz-ci-cd/
├── Jenkinsfile          # Jenkins pipeline definition for CI/CD
├── README.md            # This document
├── src/                 # Source code for the Page Object Model (POM)
│   └── Quizizz.Core/
│       ├── Quizizz.Core.csproj
│       └── Pages/
│           ├── DashboardPage.cs
│           ├── HomeworkAssignPage.cs
│           ├── LiveSessionPage.cs
│           ├── LoginPage.cs
│           ├── QuizEditorPage.cs
│           ├── ResultsPage.cs
│           └── UserProfilePage.cs
├── tests/               # Automated tests
│   └── Quizizz.Tests/
│       ├── Quizizz.Tests.csproj
│       ├── Pages/
│       │   ├── DashboardPageTests.cs
│       │   ├── HomeworkAssignPageTests.cs
│       │   ├── LiveSessionPageTests.cs
│       │   ├── LoginPageTests.cs
│       │   ├── QuizEditorPageTests.cs
│       │   ├── ResultsPageTests.cs
│       │   └── UserProfilePageTests.cs
│       └── Bdd/
│           ├── Features/
│           │   └── CreateQuiz.feature
│           └── StepDefinitions/
│               └── CreateQuizSteps.cs
└── build/
    └── nuget.config    # Example NuGet configuration (optional)
```

### `src/`

This folder contains a lightweight C# library project (`Quizizz.Core`) that
implements the Page Object Model (POM) classes for the Quizizz application.
Each class represents a page in the application (login, dashboard,
editor, etc.) and exposes methods corresponding to user actions.  The
implementation here is deliberately simple: methods update internal state
and raise exceptions when invalid data is supplied.  In your real
automation project you would replace these stubs with Selenium WebDriver
operations or calls to your preferred UI automation toolkit.

### `tests/`

The `Quizizz.Tests` project is an xUnit test project that exercises the POM
classes.  Each page class has a corresponding test class covering all
public methods, including positive and negative scenarios.  There is also
a basic BDD example using [SpecFlow](https://specflow.org/) with a Gherkin
feature file and step definitions.  If you prefer another BDD tool such as
Cucumber for JVM or pytest‑bdd for Python, you can adapt this structure.

### `Jenkinsfile`

The Jenkinsfile defines a declarative pipeline that performs the following
stages:

1. **Checkout** – clones your Git repository.
2. **Restore** – runs `dotnet restore` to download dependencies.
3. **Build** – builds the solution in Release configuration.
4. **Test** – executes unit tests with `dotnet test` and publishes
   results for Jenkins to consume.  The stage demonstrates how to generate
   Allure test results from `.trx` files using the Allure command‑line
   interface.  You need to install the Allure CLI on the Jenkins agent
   and configure the Allure Jenkins plugin to pick up results from
   `./TestResults/allure-results`.
5. **Post steps** – always collects test results and publishes Allure
   reports.

You can extend the pipeline with additional stages, for example to run
integration tests, perform code analysis, or deploy the application to a
test environment.

## How to use this project

1. **Clone the repository** into a Git server of your choice (GitHub,
   Bitbucket, GitLab, etc.).  For example:
   ```sh
   git clone https://github.com/your‑account/quizizz-ci-cd.git
   ```
   Push the code to your remote so Jenkins can access it.

2. **Install Jenkins** on your local machine or a virtual machine.  Use
   the official installer packages from <https://www.jenkins.io/>.  Once
   installed, complete the initial setup and install the following
   plugins via **Manage Jenkins → Manage Plugins**:
   - **Git** – allows Jenkins to clone Git repositories.
   - **NuGet** – for restoring NuGet packages (optional because
     `dotnet restore` is usually sufficient for .NET Core).
   - **MSBuild** – required only if you build legacy .NET Framework
     applications.  For .NET Core you can rely on `dotnet` tooling.
   - **.NET SDK** plugin (or configure `dotnet` in the Jenkins global
     tool configuration) – Jenkins needs the .NET Core SDK to run
     `dotnet restore`, `build` and `test` commands.  The SDK must be
     installed on the Jenkins agent machine.
   - **Allure** – to publish Allure reports.

3. **Configure global tools** under **Manage Jenkins → Global Tool
   Configuration**.  Set up:
   - A **Git** installation if Jenkins does not auto‑detect it.
   - A **.NET** installation (point to the `dotnet` executable on your
     agent) or install the `.NET SDK` plugin.
   - The **Allure** command‑line tool (download from
     <https://github.com/allure-framework/allure2/releases>) and configure
     it as an Allure installation.

4. **Create a new Jenkins Pipeline job**:
   - In Jenkins, click **New Item** and select **Pipeline**.
   - Give the job a name, for example `Quizizz-CI`.
   - Under **Pipeline Definition**, choose **Pipeline script from SCM**.
   - Select **Git** and provide the repository URL of your cloned project.
   - Jenkins will look for a `Jenkinsfile` at the root of the project.  You
     can change the path if necessary.

5. **Trigger the pipeline**:
   - You can configure build triggers such as `Poll SCM` (e.g. `H/5 * * * *` to
     check for changes every 5 minutes) or a GitHub web hook to start a
     build on every commit.
   - The pipeline will run the stages defined in the `Jenkinsfile`.  If
     everything is configured correctly, you will see build, test and
     Allure report results in Jenkins.

6. **Parallel test execution**:
   - The sample tests are light‑weight and run sequentially by default.  To
     enable parallel execution you can modify the `dotnet test` command in
     the Jenkinsfile with the `--parallel` option provided by xUnit.  For
     example:
     ```sh
     dotnet test --no-build --no-restore --logger:"trx;LogFileName=test_results.trx" -m:3
     ```
     The `-m:3` option tells xUnit to run up to three collections in parallel.
   - Alternatively you can run BDD tests with SpecFlow+ Runner, which
     supports parallel execution out of the box.  Modify the test
     project accordingly.

7. **BDD tests**:
   - The `features/` folder contains a single Gherkin feature file
     (`CreateQuiz.feature`) as an example.  The corresponding step
     definitions are in `StepDefinitions/CreateQuizSteps.cs`.  To use
     SpecFlow, install the `SpecFlow` and `SpecFlow.xUnit` NuGet packages
     in the `Quizizz.Tests.csproj` project.  The sample code includes
     the basic scaffolding but may require additional packages.

8. **Customisation**:
   - Replace the stub implementations in `src/Quizizz.Core` with real
     Selenium WebDriver code interacting with the Quizizz website.
   - Extend the test classes to fully cover your POM methods and add new
     tests as you expand the framework.
   - Integrate with ReportPortal or another reporting service by adding
     the appropriate packages and publishing steps in the pipeline.

## What to download

To run this project on your machine, **download or clone the repository**
from your Git server and import it into your IDE.  If you just need the
files contained here, you can download the prepared archive from this
exercise (see the attachments in the ChatGPT response) and extract it.
The archive contains all the files described above and is ready to be
committed to a repository.

Once you have the code locally, follow the steps in this README to set up
Jenkins and the pipeline.  You can then extend the framework with real
tests for the Quizizz platform and integrate additional CI/CD stages as
required.