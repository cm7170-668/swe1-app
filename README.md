# Django Polls Application

[![Build Status](https://app.travis-ci.com/cm7170-668/swe1-app.svg?branch=main)](https://app.travis-ci.com/cm7170-668/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/cm7170-668/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/cm7170-668/swe1-app?branch=main)

A Django polls application with continuous integration and deployment.

## Features

- Django web application (polls app from Django tutorial)
- Automated testing with Travis CI
- Code quality checks with Black and Flake8
- Code coverage tracking with Coveralls
- Automated deployment to AWS Elastic Beanstalk

## Development

This project uses:
- Python 3.12
- Django 5.2.7
- PostgreSQL (production)
- SQLite (development)

## CI/CD

- **Travis CI**: Automated builds and tests on every push
- **Black**: Code formatting validation
- **Flake8**: Linting and code quality checks
- **Coverage.py**: Test coverage measurement
- **Coveralls**: Coverage reporting
- **AWS Elastic Beanstalk**: Production deployment

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## Testing

Run tests with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

Check code formatting:
```bash
black --check .
flake8 .
```

## Deployment

The application automatically deploys to AWS Elastic Beanstalk when all tests pass on the main branch.

# Testing Travis CI
