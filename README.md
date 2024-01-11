# PataDoc

Bring doctors closer to you

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Directory Structire](#directory-structure)
- [Database](#database)
- [Contributions](#contributions)
- [Authors](#authors)

## About

"PataDoc" is a digital healthcare platform designed to seamlessly connect patients with a diverse range of healthcare specialists across Kenya.

## Features

- Users can search for specialists based on ther medical needs
- Patient Registration and Authentication
- Doctor Registration and Authentication
- Doctors can easily create and manage their profiles
- Patients can schedule an appointment with a specialist of choice
- Patients can review a specialist after an apppointment

## Getting Started

## Installation

To install and set up the PataDoc website locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/dmuvaa/PataDoc.git
```

2. Navigate to the project directory:

```
cd PataDoc
```

3. Activate the virtual environment (recommended):

```
source venv/bin/activate
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

To run the PataDoc website locally, follow these steps:

1. Set the necessary environment variables. For example:

```
export FLASK_APP=run
```

```
export FLASK_ENV=development
```

```
flask run
```

or you can simply run

```
python3 -m run
```

Save this in a .env file within your app folder
```
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:port/patadoc
EMAIL=your_email
PASSWORD=your_password
```

2. Initialize the database:

```
flask db init
```

3. Apply the database migrations:

```
flask db migrate
```

```
flask db upgrade
```

4. Start the Flask development server:

```
flask run
```

5. Access the website in your browser at `http://localhost:5000`.

## Directory Structure

The directory structure of the PataDoc website is as follows:

```
├── README.md
├── __init__.py
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── admin_auth.py
│   │   ├── doctor_auth.py
│   │   ├── routes.py
│   │   ├── user.py
│   │   └── user_auth.py
│   ├── db.py
│   ├── models.py
│   ├── static
│   │   ├── avatar1.png
│   │   ├── doctor_profile
│   │   ├── images
│   │   ├── js
│   │   │   └── find_doctors.js
│   │   ├── styles
│   │   │   ├── base.css
│   │   │   ├── login.css
│   │   │   ├── pending_doctors.css
│   │   │   ├── sign_up.css
│   │   │   └── specialists.css
│   │   └── user_profile
│   ├── templates
│   │   ├── admin_signup.html
│   │   ├── base.html
│   │   ├── book_appointment.html
│   │   ├── display.html
│   │   ├── doctor_profile.html
│   │   ├── doctor_sign_up.html
│   │   ├── doctors_by_specialization.html
│   │   ├── find_doctors.html
│   │   ├── home.html
│   │   ├── leave_review.html
│   │   ├── login.html
│   │   ├── patient_profile.html
│   │   ├── pending_doctors.html
│   │   ├── sign_up.html
│   │   ├── specialists.html
│   │   └── specializations.html
│   └── views
│       ├── __init__.py
│       └── routes.py
├── migrations
│   └── versions
├── requirements.txt
└── run.py
```

- The `run.py` file serves as the entry point of the Flask application.
- The `migrations/versions` contains the versions of the database used by the application.
- The `models.py` file defines the classes representing the database tables.
- The `views.py` file contains all the routes for viewing.
- The `db.py` file contains all the assistant functions.

## Database

The PataDoc website uses a PostgreSQL database managed by Flask SQLAlchemy. The database versions are in the migrations folder.

## Contributions

Contributions to the PataDoc website are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

---

## Authors

1. Winfred Kiarie - [Github](https://github.com/epicsociety)
3. Dennis Muvaa - [Github](https://github.com/dmuvaa)
2. Prisca Ndiritu - [Github](https://github.com/ndiritu-prisca)

Thank you for your interest in the PataDoc website! If you have any further questions or need assistance, please feel free to contact us.
