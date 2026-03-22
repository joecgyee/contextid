# ContextID

*Adaptive Identity made simple.*

**ContextID** is a privacy-focused identity and profile management system. It allows users to create **context-specific identity profiles** (*e.g., Legal, Professional, Social*) and share them via a controlled REST API.

## Key Features

* **Contextual Profiles:** Maintain separate display names, profile pictures, and attributes for different life contexts.
* **Dynamic Attributes:** Add typed attributes (Strings, Integers, Booleans, Dates, URLs) to profiles without database schema alterations.
* **Privacy-First Design:** Toggle profiles between Public and Private. Private profiles are strictly protected via JWT.
* **Seamless UI/UX:** Built with Django templates, Bootstrap 5, and JavaScript for dynamic front-end interactions (dynamic formsets, instant previews).
* **Developer Friendly API:** Native Django REST Framework (DRF) endpoints for resolving identity programmatically.

## Live Demo
Check out the live app [here](https://contextid.onrender.com).

## Getting Started 

### Prerequisites

* Python 3.10 or higher
* Git
* PostgreSQL

### Local Installation

```bash
# Clone the repository
git clone https://github.com/joecgyee/contextid.git
cd contextid

# Set up a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Go to project root directory
cd contextid

# Install dependencies
pip install -r requirements.txt

# Run psql to setup database
psql -U {your_username} -f setup_db.sql

# Environment configuration, create a `.env` file in the root directory
SECRET_KEY=your-local-secret-key
DEBUG=True

# Run migrations & Seed data
python manage.py makemigrations 
python manage.py migrate 

# Start the local server
python manage.py runserver

# Running tests
python manage.py test 

# Run tests for a specific app (e.g. profiles)
python manage.py test apps.profiles
```

### API Quickstart

1. Obtain a Token 
`POST /api/v1/login/`
2. Query identity context resolution
`GET /api/v1/identity/?user={user.username}&context={context.name}`
