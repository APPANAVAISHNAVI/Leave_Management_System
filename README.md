# 🧾 Employee Leave Management System

A **Flask-based web application** that allows employees to apply for leave and managers to review, approve, or reject leave requests.  
This system simplifies leave tracking, improves transparency, and provides a clean web interface for both employees and managers.

---

## 🚀 Features

### 👩‍💼 Employee Features
- Register and log in securely  
- Apply for leave with start/end dates and reason  
- View leave history and current status  
- Receive status updates when approved/rejected  

### 👨‍💼 Manager/Admin Features
- Log in as a manager  
- View all employee leave requests  
- Filter leaves by employee name, email, or status  
- Approve or reject requests with comments  
- Manage leave history efficiently  

---

## 🏗️ Tech Stack

| Layer | Technology |
|--------|-----------|
| **Frontend** | HTML, CSS |
| **Backend** | Flask (Python) |
| **Database** | SQLite |
| **ORM** | SQLAlchemy |
| **Forms** | Flask-WTF |
| **Authentication** | Flask-Login |
| **Environment** | Python 3.10+ |

---

## ⚙️ Installation and Setup (PyCharm or CLI)

1. **Clone this repository**
   ```bash
   git clone https://github.com/APPANAVAISHNAVI/Leave_Management_System.git
   cd Leave_Management_System
2. **Create a virtual environment**
    ```bash
    python -m venv .venv
   .venv\Scripts\activate      # On Windows
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Initialize Database**
   ```bash
   flask shell
>>> from app import create_app
>>> from extensions import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
5. **Run the Application**
   ```bash
   python app.py
| Role              | Description                                                       |
| ----------------- | ----------------------------------------------------------------- |
| **Employee**      | Can register, log in, and apply for leave                         |
| **Manager/Admin** | Can log in, view all leave requests, approve/reject with comments |

📂 Project Structure
Leave_Management_System/
├── app.py
├── config.py
├── extensions.py
├── forms.py
├── models.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── apply_leave.html
│   ├── admin_dashboard.html
│   └── _fragments.html
└── tests/
    └── test_basic.py


