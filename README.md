# Career Opportunities Management System

## Description
This project is a Flask-based web application developed for managing career opportunities. It allows users to create, view, update, and delete opportunities, as well as apply to them. The system also includes a REST API and a comprehensive testing suite that demonstrates different software testing techniques.

## Features
- Create, view, update, and delete career opportunities (CRUD)
- Apply to opportunities with applicant details
- View submitted applications
- REST API for managing opportunities (GET, POST, PUT, DELETE)
- Input validation and error handling
- Clean and user-friendly interface
- Automated testing with pytest:
  - Unit tests
  - Integration tests
  - System test
  - REST API tests
  - Mock and patch testing

## Technologies Used
- Python
- Flask
- SQLAlchemy / Flask-SQLAlchemy
- SQLite
- HTML and CSS
- Pytest
- unittest.mock
- Git and GitHub

## Project Structure
project-folder/
│
├── app.py                # Main application (routes + API)
├── models.py             # Database models
├── utils.py              # Helper functions (notifications)
├── requirements.txt      # Dependencies
│
├── templates/            # HTML templates
│   ├── index.html
│   ├── add_opportunity.html
│   ├── edit_opportunity.html
│   ├── apply_opportunity.html
│   └── applications.html
│
├── static/               # CSS styling
│   └── styles.css
│
├── tests/                # Test files
│   ├── test_basic.py
│   ├── test_unit.py
│   ├── test_integration.py
│   ├── test_system.py
│   └── test_mock_patch.py
│
└── README.md

## Installation and Setup

1. Clone the repository:
git clone https://github.com/ooddetaa/career-opportunities-project.git

2. Navigate to the project folder:
cd career-opportunities-project

3. Create a virtual environment:
python -m venv venv

4. Activate the virtual environment:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

5. Install dependencies:
pip install -r requirements.txt

## Running the Application

Run the application using:
python app.py

Then open your browser and go to:
http://127.0.0.1:5000

## Running Tests

To run all tests:
python -m pytest

All tests should pass successfully.

## API Endpoints

- GET /api/opportunities → Get all opportunities
- GET /api/opportunities/<id> → Get single opportunity
- POST /api/opportunities → Create opportunity
- PUT /api/opportunities/<id> → Update opportunity
- DELETE /api/opportunities/<id> → Delete opportunity

## Testing Overview

The project includes multiple types of testing:
- Unit testing for small functions
- Integration testing for database and routes
- System testing for full user flow
- REST API testing for endpoints
- Mock and patch testing for external functionality simulation

## Author
Odeta Haxhihasani