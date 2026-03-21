# ContextID

Adaptive Identity made simple.

## Prerequisites

This project is developed with:

- **Operating System**: Windows 11  
- **Python Version**: 3.13.2
- **Django Version**: 6.0
- **Package Managers**: pip & virtualenv
- **Database**: PostgreSQL

## Installation

```bash
# Clone the repo
git clone
cd contextid

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Go to project root directory
cd contextid

# Run psql to setup database
psql -U postgres -f setup_db.sql

python manage.py makemigrations 
python manage.py migrate 

# Run server
python manage.py runserver

# Run all tests
python manage.py test 

# Run tests for a specific app (e.g. profiles)
python manage.py test apps.profiles

```
