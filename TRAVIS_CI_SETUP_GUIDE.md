# Travis CI Setup Guide for Django Project

This guide will walk you through setting up Continuous Integration and Continuous Deployment (CI/CD) for your Django polls application using Travis CI.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Configuration Files Explained](#configuration-files-explained)
5. [Testing Locally](#testing-locally)
6. [Troubleshooting](#troubleshooting)

---

## Overview

### What We're Setting Up
- **Travis CI**: Automatically builds and tests your code on every push/PR
- **Black**: Code formatter that ensures consistent code style
- **Flake8**: Linter that checks for code quality issues
- **Coverage.py**: Measures how much of your code is covered by tests
- **Coveralls**: Displays code coverage reports online
- **AWS Elastic Beanstalk Deployment**: Automatically deploys to AWS on successful builds

### How It Works
1. You push code to GitHub
2. Travis CI detects the push and starts a build
3. Travis runs: Black → Flake8 → Tests with Coverage
4. If all checks pass, Travis deploys to AWS Elastic Beanstalk
5. Coverage report is sent to Coveralls
6. Build status badges update on your README

---

## Prerequisites

Before starting, ensure you have:
- ✅ Django polls app in a GitHub repository
- ✅ App already deployed to AWS Elastic Beanstalk
- ✅ GitHub account with admin access to your repository
- ✅ AWS account with Elastic Beanstalk app running

---

## Step-by-Step Setup

### STEP 1: Sign Up for Travis CI

1. Go to https://travis-ci.com/
2. Click "Sign up with GitHub"
3. Authorize Travis CI to access your GitHub account
4. Accept the GitHub permissions

**What this does**: Connects Travis CI to your GitHub account so it can monitor your repositories.

---

### STEP 2: Activate Your Repository on Travis CI

1. Once logged into Travis CI, click your profile picture (top right)
2. Click "Settings"
3. Find your Django project repository in the list
4. Toggle the switch to **ON** (green)

**What this does**: Tells Travis CI to watch this specific repository and run builds when you push code.

---

### STEP 3: Get Your AWS Elastic Beanstalk Information

You need to gather some information about your existing AWS EB deployment:

1. **AWS Region**: Where your EB app is hosted (e.g., `us-east-1`, `us-west-2`)
   - Find this in AWS Console → Elastic Beanstalk → Your Environment

2. **Application Name**: Your EB application name
   - Find this in AWS Console → Elastic Beanstalk → Applications

3. **Environment Name**: Your EB environment name
   - Find this in AWS Console → Elastic Beanstalk → Environments

**Write these down - you'll need them in the next step!**

---

### STEP 4: Update .travis.yml with Your AWS Information

Open the `.travis.yml` file and update these lines:

```yaml
deploy:
  provider: elasticbeanstalk
  region: "us-east-1"  # ← Change to YOUR AWS region
  app: "your-app-name"  # ← Change to YOUR EB application name
  env: "your-env-name"  # ← Change to YOUR EB environment name
  bucket_name: "elasticbeanstalk-us-east-1-YOUR-ACCOUNT-ID"  # ← Optional: Travis can auto-create
  bucket_path: "your-app-name"  # ← Should match your app name
  on:
    branch: main  # ← Change to "master" if that's your main branch
```

**What this does**: Tells Travis where to deploy your app after successful tests.

---

### STEP 5: Create AWS IAM User for Travis CI

Travis needs AWS credentials to deploy to Elastic Beanstalk. Create a dedicated IAM user:

1. Go to AWS Console → IAM → Users → Add User
2. User name: `travis-ci-deployer`
3. Access type: ✅ Programmatic access
4. Click "Next: Permissions"
5. Click "Attach existing policies directly"
6. Search for and select these policies:
   - `AWSElasticBeanstalkFullAccess`
   - `AmazonS3FullAccess` (needed for deployment artifacts)
7. Click "Next" through to "Create user"
8. **IMPORTANT**: Copy the **Access Key ID** and **Secret Access Key**
   - You won't be able to see the secret key again!

**What this does**: Creates a user account that Travis CI will use to deploy to AWS on your behalf.

---

### STEP 6: Add AWS Credentials to Travis CI (Securely)

**NEVER put your AWS credentials directly in .travis.yml!** Use Travis environment variables:

1. Go to Travis CI → Your Repository → More Options → Settings
2. Scroll to "Environment Variables"
3. Add two variables:

   **Variable 1:**
   - Name: `AWS_ACCESS_KEY_ID`
   - Value: [paste your Access Key ID from Step 5]
   - ✅ Display value in build log: **OFF** (keep it secret!)
   - Click "Add"

   **Variable 2:**
   - Name: `AWS_SECRET_ACCESS_KEY`
   - Value: [paste your Secret Access Key from Step 5]
   - ✅ Display value in build log: **OFF** (keep it secret!)
   - Click "Add"

**What this does**: Securely stores your AWS credentials so Travis can deploy without exposing them in your code.

---

### STEP 7: Sign Up for Coveralls

1. Go to https://coveralls.io/
2. Click "Sign in with GitHub"
3. Authorize Coveralls to access your GitHub
4. Click "Add Repos"
5. Find your repository and toggle it **ON**
6. Click on your repository name in Coveralls
7. Copy your **repo_token** (you'll see it on the repo page)

**Optional**: Add the repo token to Travis CI:
- Go to Travis CI → Your Repository → Settings → Environment Variables
- Add variable: `COVERALLS_REPO_TOKEN` with your token value

**What this does**: Sets up code coverage tracking and reporting for your project.

---

### STEP 8: Add Badges to Your README.md

Create or update your README.md file with status badges. Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME`:

```markdown
# Django Polls Application

[![Build Status](https://app.travis-ci.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.svg?branch=main)](https://app.travis-ci.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME)
[![Coverage Status](https://coveralls.io/repos/github/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/badge.svg?branch=main)](https://coveralls.io/github/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME?branch=main)

Your project description here...
```

**Example** (if your GitHub username is `jdoe` and repo is `django-polls`):
```markdown
[![Build Status](https://app.travis-ci.com/jdoe/django-polls.svg?branch=main)](https://app.travis-ci.com/jdoe/django-polls)
[![Coverage Status](https://coveralls.io/repos/github/jdoe/django-polls/badge.svg?branch=main)](https://coveralls.io/github/jdoe/django-polls?branch=main)
```

**What this does**: Displays live build status and code coverage percentage on your README.

---

### STEP 9: Enable Branch Protection on GitHub

This ensures PRs can't be merged unless Travis CI checks pass:

1. Go to your GitHub repository
2. Click "Settings" (repository settings, not your account)
3. Click "Branches" in the left sidebar
4. Under "Branch protection rules", click "Add rule"
5. Branch name pattern: `main` (or `master` if that's your main branch)
6. Check these boxes:
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - In the search box that appears, type "Travis CI" and select it
   - ✅ **Include administrators** (optional but recommended)
7. Click "Create" or "Save changes"

**What this does**: Prevents merging code that fails Travis CI checks (failing tests, linting errors, etc.).

---

### STEP 10: Push Your Changes to GitHub

Commit and push all the configuration files:

```bash
git add .travis.yml .flake8 .coveragerc requirements.txt README.md
git commit -m "Add Travis CI configuration for automated testing and deployment"
git push origin main
```

**What this does**: Triggers your first Travis CI build!

---

### STEP 11: Monitor Your First Build

1. Go to https://travis-ci.com/
2. Click on your repository
3. You should see a build running (yellow/orange indicator)
4. Click on the build to see real-time logs

**What to expect**:
- Travis will install dependencies
- Run Black (code formatting check)
- Run Flake8 (linting)
- Run tests with coverage
- Send coverage to Coveralls
- Deploy to AWS (if all checks pass)

---

## Configuration Files Explained

### .travis.yml (Travis CI Configuration)

```yaml
language: python
```
Tells Travis this is a Python project.

```yaml
python:
  - "3.12"
```
Specifies Python 3.12 for testing.

```yaml
services:
  - postgresql
```
Starts a PostgreSQL database for testing (matches your production setup).

```yaml
cache:
  directories:
    - $HOME/.cache/pip
```
Caches pip packages between builds to speed up installation.

```yaml
install:
  - pip install -r requirements.txt
  - pip install black flake8 coverage coveralls
```
Installs your project dependencies and CI/CD tools.

```yaml
before_script:
  - psql -c 'create database test_db;' -U postgres
```
Creates a test database before running tests.

```yaml
script:
  - black --check .
  - flake8 .
  - coverage run --source='.' manage.py test
  - coverage report
```
**The main checks**:
1. `black --check .`: Checks if code is formatted correctly (doesn't modify files)
2. `flake8 .`: Checks for code quality issues
3. `coverage run`: Runs Django tests while measuring code coverage
4. `coverage report`: Displays coverage summary

```yaml
after_success:
  - coveralls
```
Sends coverage data to Coveralls after successful tests.

```yaml
deploy:
  provider: elasticbeanstalk
  ...
```
Deploys to AWS Elastic Beanstalk if all tests pass.

---

### .flake8 (Flake8 Linter Configuration)

```ini
[flake8]
max-line-length = 88
```
Sets maximum line length to 88 characters (matches Black's default).

**Why 88?** Black uses 88 as a compromise between readability and compactness.

```ini
extend-ignore =
    E203,  # whitespace before ':'
    W503   # line break before binary operator
```
Ignores specific rules that conflict with Black's formatting.

```ini
exclude =
    migrations,
    venv,
    ...
```
Tells Flake8 to skip checking these directories (they're auto-generated or third-party code).

---

### .coveragerc (Coverage.py Configuration)

```ini
[run]
branch = True
```
Measures both line coverage and branch coverage (more thorough).

```ini
omit =
    */migrations/*
    */tests.py
    ...
```
Excludes files from coverage measurement (migrations are auto-generated, tests test themselves).

```ini
[report]
show_missing = True
```
Shows which specific lines weren't covered by tests.

---

## Testing Locally

Before pushing to GitHub, test locally to catch errors early:

### 1. Install CI/CD tools locally:
```bash
pip install black flake8 coverage
```

### 2. Check code formatting:
```bash
black --check .
```
**Expected output**: "All done! ✨ 🍰 ✨" or a list of files that need formatting.

**To auto-format** (if you want):
```bash
black .
```

### 3. Check linting:
```bash
flake8 .
```
**Expected output**: Nothing (silence means success!) or a list of issues to fix.

**Common issues**:
- Unused imports
- Variables defined but never used
- Lines too long
- Missing whitespace

**To fix specific line** (if you disagree with flake8):
```python
# Add this comment at the end of the line
x = some_long_function_call()  # noqa: E501
```

### 4. Run tests with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```
**Expected output**: Test results and coverage percentage.

### 5. View detailed coverage report (HTML):
```bash
coverage html
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

---

## Troubleshooting

### Issue: "black --check" fails

**Symptom**: Travis fails with "would reformat" messages.

**Solution**: Run `black .` locally to auto-format your code, then commit:
```bash
black .
git add .
git commit -m "Format code with black"
git push
```

---

### Issue: Flake8 errors

**Symptom**: Travis fails with flake8 violations.

**Solution 1** - Fix the issues:
```bash
flake8 .  # See what's wrong
# Fix the issues in your code
```

**Solution 2** - Ignore specific lines (use sparingly):
```python
import something_needed  # noqa: F401
```

**Common flake8 codes**:
- `E501`: Line too long (should be rare with black)
- `F401`: Module imported but unused
- `F841`: Variable assigned but never used
- `E302`: Expected 2 blank lines, found 1

---

### Issue: Coverage too low

**Symptom**: Coverage report shows low percentage.

**Solution**: Add more tests! For the homework, actual tests aren't required yet, but you can add basic tests:

```python
# polls/tests.py
from django.test import TestCase
from .models import Question

class QuestionModelTests(TestCase):
    def test_string_representation(self):
        question = Question(question_text="Test question")
        self.assertEqual(str(question), "Test question")
```

---

### Issue: Travis deployment fails

**Symptom**: Tests pass but deployment to AWS fails.

**Possible causes**:
1. Wrong AWS region/app name/env name in `.travis.yml`
2. AWS credentials not set or incorrect
3. IAM user doesn't have proper permissions

**Solution**:
1. Double-check your `.travis.yml` AWS settings
2. Verify environment variables in Travis CI settings
3. Check IAM user has `AWSElasticBeanstalkFullAccess` and `AmazonS3FullAccess`

---

### Issue: PostgreSQL errors in Travis

**Symptom**: Database connection errors during tests.

**Solution**: The configuration should work, but if you see issues, your tests might be using SQLite (default for testing):

In settings.py, Django automatically uses SQLite for tests even if production uses PostgreSQL. This is fine for the homework.

---

### Issue: Travis build doesn't start

**Symptom**: You pushed code but Travis isn't building.

**Solution**:
1. Check that your repo is activated in Travis CI settings
2. Check that `.travis.yml` is in the root directory
3. Check `.travis.yml` syntax (use http://www.yamllint.com/)
4. Try pushing a new commit

---

### Issue: Coveralls not showing coverage

**Symptom**: Tests pass but no coverage on Coveralls.

**Solution**:
1. Ensure your repo is activated on coveralls.io
2. Check Travis logs to see if `coveralls` command succeeded
3. Verify `COVERALLS_REPO_TOKEN` is set (if private repo)

---

## Submission Checklist

Before submitting, verify:

- ✅ Travis CI is running builds on your repo
- ✅ `.travis.yml` file is present and configured correctly
- ✅ `.flake8` file is present
- ✅ `.coveragerc` file is present
- ✅ `requirements.txt` includes black, flake8, coverage, coveralls
- ✅ Build status badge appears on README.md
- ✅ Coverage badge appears on README.md
- ✅ Branch protection is enabled on GitHub
- ✅ Travis CI Dashboard URL is ready to submit

**Your Travis Dashboard URL** will be:
```
https://app.travis-ci.com/github/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME
```

---

## Testing the Definition of DONE

As the assignment states, you're done when:

### ✅ Test 1: Open a PR and see Travis run
```bash
# Create a test branch
git checkout -b test-ci
# Make a small change
echo "# Test PR" >> README.md
git add README.md
git commit -m "Test Travis CI on PR"
git push -u origin test-ci
# Go to GitHub and create a PR from test-ci to main
# You should see Travis CI checks running!
```

### ✅ Test 2: Introduce a linting error (should fail)
```python
# In any .py file, add:
import os  # Import but don't use it
x=1+2  # No spaces around operators
```
Push this - Travis should mark the build as "failed" (red) due to flake8 violations.

### ✅ Test 3: Fix and see it pass
Remove the bad code, push again - Travis should pass (green).

### ✅ Test 4: Verify deployment
After a successful build on `main` branch, check your AWS EB environment - the app should be updated.

---

## Additional Resources

- Travis CI Docs: https://docs.travis-ci.com/
- Black Documentation: https://black.readthedocs.io/
- Flake8 Documentation: https://flake8.pycqa.org/
- Coverage.py Documentation: https://coverage.readthedocs.io/
- Coveralls Documentation: https://docs.coveralls.io/
- AWS EB Deployment: https://docs.travis-ci.com/user/deployment/elasticbeanstalk/

---

## Questions?

Common questions:

**Q: Do I need to write actual tests?**
A: For this homework, no unit tests are required yet, but they're welcomed. The basic test structure is enough.

**Q: What if my coverage is 0%?**
A: That's okay for now! As long as the coverage report runs successfully, you're good.

**Q: Can I use Travis CI for private repos?**
A: Yes! Travis CI supports private repos. You might need to use travis-ci.com (not travis-ci.org).

**Q: What if I use `master` instead of `main`?**
A: Just change `branch: main` to `branch: master` in `.travis.yml` and in the branch protection settings.

---

Good luck with your CI/CD setup! 🚀
