# Event Management System (MySQL)

This project is a small Flask app for managing events, venues, participants, and registrations. It was migrated from SQLite to MySQL. Below are quick setup instructions for Windows (PowerShell).

Prerequisites
- Python 3.8+
- MySQL server (local or remote)

1) Create a Python virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Set environment variables (PowerShell example)

```powershell
$env:MYSQL_USER = 'your_mysql_user'
$env:MYSQL_PASSWORD = 'your_password'
$env:MYSQL_HOST = '127.0.0.1'
$env:MYSQL_PORT = '3306'
$env:MYSQL_DATABASE = 'event_management'
```

3) Initialize the database schema

Run the `data.py` script which will create the database and tables if they don't exist:

```powershell
python data.py
```

4) Run the Flask app

```powershell
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'development'
flask run
```

Notes
- The app reads database configuration from environment variables. If you prefer, create a `.env` file and load it before running.
- Default MySQL database name is `event_management`.

If you want, I can also add a small helper script to load sample data or a `.env` file template.
