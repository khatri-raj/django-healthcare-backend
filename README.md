# Django Healthcare Backend

Backend system for a healthcare app built with Django and Django REST Framework.

## Features
- JWT Authentication
- CRUD APIs for Patients and Doctors
- Patient-Doctor Mapping
- PostgreSQL database
- Tested using Postman

## APIs
1. `/api/auth/register/`
2. `/api/auth/login/`
3. `/api/patients/`
4. `/api/doctors/`
5. `/api/mappings/`

## Run Locally
1. Create a virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Set up `.env` for secret keys and database
4. Run migrations: `python manage.py migrate`
5. Run server: `python manage.py runserver`
