# CivicFix
## Features
- User authentication
- Complaint reporting
- Image upload
- Admin dashboard
- Search & filtering
- Analytics charts
- Complaint status management


A simple and minimal system to report public problems.

How to Run the Project

1. Clone the repository

git clone <your-github-link>
cd project-folder

2. Create virtual environment

python -m venv venv

3. Activate virtual environment

Windows

venv\Scripts\activate

Linux/Mac

source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Configure MySQL

Open "setup_db.py" and change:

host="localhost"
user="your_mysql_username"
password="your_mysql_password"

according to your local MySQL setup.

6. Run database setup

python setup_db.py

This will create the database and required tables automatically.

7. Run the Flask app

python run.py
