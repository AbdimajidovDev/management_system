
# 🎓 Learning Center Management System

> A web-based management system for educational centers built with **Django & DRF**.
> It provides powerful tools for admins, teachers, and parents to manage groups, students, attendance, payments, and reports efficiently.

---

## ✨ Key Features

* 👩‍🏫 **User Roles**: Superadmin, Admin, Teacher, Parent
* 🏫 **Group Management**: Create groups, assign teachers, set prices, track start/end dates
* 📚 **Student Management**: Register students, assign to groups, link with parents, payment status
* ✅❌🔳 **Attendance System**: Track attendance with present/absent/empty status
* 💰 **Payments**: Tuition fees for groups, payment tracking, teacher salaries (50% of revenue)
* 📊 **Reports & Analytics**: Teacher salaries, attendance statistics, top students, income reports
* 🗓 **Lesson Scheduling**: Automatically generated lessons based on odd/even weekdays
* 🎨 **Modern Admin UI**: Built with `django-unfold` for a clean and responsive admin interface
* 🔐 **Security**: Role-based permissions and restricted access control

---

## 🛠 Tech Stack

* **Backend**: Django, Django REST Framework
* **Database**: PostgreSQL / SQLite (for development)
* **Admin UI**: Django Unfold
* **API Documentation**: DRF Spectacular (`/api/schema/swagger-ui/`)
* **Authentication**: JWT (`djangorestframework-simplejwt`)

---

## 📂 Main Modules

1. **User** – User roles (superadmin, admin, teacher, parent)
2. **Group** – Group management (teacher, pricing, type, dates)
3. **Student** – Student and parent relationships
4. **Attendance** – Daily attendance system (✅, ❌, 🔳)
5. **Reports** – Insights, statistics, and charts
6. **Payments** – Student tuition & teacher salary calculations

---

## 🚀 Installation

### 1. Clone the repository

```bash

git clone hhttps://github.com/AbdimajidovDev/management_system.git
```

### 2. Create a virtual environment

```bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash

pip install -r requirements.txt
```

### 4. Apply migrations

```bash

python manage.py migrate
```

### 5. Create superuser

```bash

python manage.py createsuperuser
```

### 6. Run development server

```bash

python manage.py runserver
```

---

## 🔗 API Documentation

* Swagger UI → `/api/schema/swagger-ui/`
* Redoc → `/api/schema/redoc/`

