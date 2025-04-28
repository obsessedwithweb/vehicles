# Vehicle Store Project

A Django-based vehicle store application with vehicle listing, shopping cart functionality, checkout process, and user authentication.

## Installation and Setup Instructions

### Prerequisites
- Python 3.x installed
- Git installed

### Step 1: Clone the Repository
```
git clone https://github.com/obsessedwithweb/vehicles.git
cd vehicles
```

### Step 2: Create and Activate a Virtual Environment
#### For Windows:
```
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
Create a `.env` file in the root directory with the following content:
```
SECRET_KEY='django-insecure-ut95j890s2&!3+*_y=kb3spq*imm&d=$i*ni_db=-#o)=pdpr+'
DEBUG=1
```

### Step 5: Run Database Migrations
```
cd src
python manage.py migrate
```

### Step 6: Create a Superuser (Optional)
```
python manage.py createsuperuser
```

### Step 7: Run the Development Server
```
python manage.py runserver
```

### Step 8: Access the Application
- Main website: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Project Features
- Vehicle listing and management
- Shopping cart functionality
- Checkout process
- User authentication (using django-allauth)
