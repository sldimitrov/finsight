# FinSight

A personal finance tracker built with Django. FinSight brings your accounts and transactions into one place so you can see where your money is and where it goes.

![FinSight MVP](docs/finsight-mvp.jpeg)

## Features

- **Accounts**: create, edit and deactivate checking, savings, credit and investment accounts
- **Transactions**: record income, expenses, transfers and adjustments; balances update automatically
- **Filtering**: browse and filter transactions across accounts
- **Data isolation**: every user sees only their own accounts and transactions
- **Immutable history**: transactions can't be edited after they're created, only deleted

## Tech stack

- Python / Django 6
- PostgreSQL
- django-environ for configuration
- django-debug-toolbar and django-extensions for development

## Getting started

### Prerequisites

- Python 3.12+
- PostgreSQL running locally

### Setup

```powershell
git clone <repo-url>
cd finsights
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy the example environment file and fill in your values:

```powershell
copy .env.example .env
```

| Variable        | Description                                              |
| --------------- | -------------------------------------------------------- |
| `DEBUG`         | `on` for local development                               |
| `SECRET_KEY`    | Django secret key                                        |
| `ALLOWED_HOSTS` | Comma-separated hosts, e.g. `localhost,127.0.0.1`        |
| `DATABASE_URL`  | `postgres://USER:PASSWORD@HOST:PORT/NAME`                |

Create the database, then run migrations and start the server:

```powershell
python manage.py migrate
python manage.py runserver
```

The app is at http://127.0.0.1:8000/.

### Sample data

To fill the database with an `admin` superuser, an account and test transactions:

```powershell
python manage.py seed_data --count 1000
```

## Running tests

```powershell
python manage.py test
```

## Project structure

```
core/          Project settings and root URLs
users/         Custom user model
accounts/      Accounts, login/logout, base templates and styles, seed command
transactions/  Transactions, filtering and balance updates
docs/          Coursework docs: requirements, architecture, ER and use-case diagrams
```

## Documentation

Design notes are in [`docs/`](docs/):

- [Problem definition](docs/problem-definition.md)
- [Functional requirements](docs/functional-requirements.md)
- [System architecture](docs/high-level-system-architecture.md)
- [Entity-relationship diagram](docs/entity-relationship-diagram.md)
- [Initial API design](docs/initial-api-design.md)
