# Django Template by Hamasakis

This repository contains a robust and configured template to kickstart new Django projects quickly. Developed by Hamasakis, this boilerplate integrates best practices and essential tools for modern applications, focusing on scalability and ease of development.

## 🚀 Features and Technologies

This template comes pre-configured with a powerful stack:

- **Backend Framework**: [Django](https://www.djangoproject.com/) (v5.2+) - The web framework for perfectionists with deadlines.
- **REST API**: [Django REST Framework](https://www.django-rest-framework.org/) - Powerful and flexible toolkit for building Web APIs.
- **Task Queue & Async**: [Celery](https://docs.celeryq.dev/) - Distributed asynchronous task queue.
- **Scheduling**: [Django Celery Beat](https://django-celery-beat.readthedocs.io/) - Periodic task scheduling.
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Advanced open source relational database.
- **Message Broker**: [RabbitMQ](https://www.rabbitmq.com/) - Robust and scalable open source message broker for Celery.
- **Caching**: [Redis](https://redis.io/) - In-memory data structure store, used for caching.
- **Admin Interface**: [Django Jazzmin](https://github.com/farridav/django-jazzmin) - Modern and customizable admin theme for Django Admin.
- **Containerization**: [Docker](https://www.docker.com/) & Docker Compose - Isolated and reproducible development environment.

## 📋 Prerequisites

Ensure you have the following installed on your machine:

- [Python 3.10+](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Git](https://git-scm.com/)

## 🛠️ Installation and Setup

Follow the steps below to set up the development environment:

### 1. Clone the repository

```bash
git clone <repository-url>
cd <directory-name>
```

### 2. Configure the Virtual Environment

It is recommended to use a virtual environment to isolate project dependencies.

```bash
python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requiriments.txt
```

> **Note**: The requirements file is named `requiriments.txt`.

### 4. Initialize Services (Docker)

Use Docker Compose to start the infrastructure services (PostgreSQL, Redis, RabbitMQ, etc.).

```bash
docker-compose up -d
```

### 5. Apply Migrations

Set up the initial database:

```bash
python manage.py migrate
```

### 6. Create a Superuser

To access the admin panel:

```bash
python manage.py createsuperuser
```

## ▶️ Running the Project

### Development Server

To run the Django application:

```bash
python manage.py runserver
```

Access at: `http://localhost:8000`

### Celery Worker

To process background tasks:

```bash
celery -A core worker -l info
```

### Celery Beat

For periodic task scheduling:

```bash
celery -A core beat -l info
```

## 📂 Project Structure

```plaintext
.
├── core/                # Main project settings (settings, urls, celery, wsgi/asgi)
├── docker-compose.yml   # Container orchestration (Postgres, RabbitMQ, etc.)
├── manage.py            # Django command-line utility
├── requiriments.txt     # Python project dependencies
└── readme.md            # Project documentation
```

## ⚙️ Important Configurations

- **Settings**: Main settings are located in `core/settings.py`.
- **Database**: Configured to connect to PostgreSQL running in Docker.
- **Celery**: Configured in `core/celery.py` using RabbitMQ as the broker.
- **Jazzmin**: The admin interface already has the Jazzmin theme applied.

## 🤝 Contribution

Feel free to fork this template and adapt it to your needs. Pull requests are welcome.

---
Developed by **Hamasakis**.
