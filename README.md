# Flask MongoDB Authentication App

A simple web application that provides user authentication (login, logout, register) using Flask and MongoDB Atlas.

## Project Structure

```
├── app.py
├── app/
│   ├── models/
│   │   └── user.py
│   ├── routes.py
│   ├── static/
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       └── register.html
├── requirements.txt
└── README.md
```

## Prerequisites

-   Python 3.6+
-   MongoDB Atlas account

## Setup

1. Clone the repository
2. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Configure MongoDB Atlas:
    - Create a MongoDB Atlas cluster
    - Create a database called `userdb`
    - Update the MongoDB connection string in `app.py` and `app/models/user.py`:
        ```python
        MONGO_URI = "mongodb+srv://your_username:your_password@your_cluster.mongodb.net/userdb?retryWrites=true&w=majority"
        ```

## Running the Application

```
python app.py
```

The application will be available at http://localhost:8000

## Features

-   User registration with username, password, and name
-   User login with username and password
-   Session management
-   User dashboard
-   Logout functionality

## Technologies Used

-   Flask: Web framework
-   PyMongo: MongoDB driver
-   bcrypt: Password hashing
-   Tailwind CSS: Styling (via CDN)
