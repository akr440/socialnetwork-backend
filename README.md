# 🌐 SocialNetwork Backend

A scalable, real-time backend for a modern social networking platform—built with Django, Django Channels, and Docker. This project powers core social features like user profiles, posts, likes, comments, polls, and both private and group messaging with WebSocket support.

---

## 🚀 Features

- 🔐 User authentication and account management
- 🧑‍🤝‍🧑 Follow system for user profiles
- 📝 Create and interact with posts (likes, comments)
- 📊 Polls for users
- 💬 Real-time private and group chat using WebSockets
- 🧠 Modular Django apps for clean separation of concerns
- 🐳 Dockerized for easy local development and future deployment

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/socialnetwork-backend.git
cd socialnetwork-backend
```

### 2. Create Your .env File
```bash
cp .env.template .env
```
Fill in your environment variables like DJANGO_SECRET_KEY, DEBUG, etc



### 3. Build and Run with Docker
```bash
docker-compose build
docker-compose up
```

### 4. Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

## 🧱 🛠️ Tech Stack
This project is built using a modern, modular backend architecture designed for scalability and real-time performance.
🔧 Core Frameworks & Libraries
- Django 5.2 – The primary web framework powering the backend logic.
- Django REST Framework – Provides a flexible and powerful toolkit for building RESTful APIs.
- Django Channels – Adds asynchronous capabilities and WebSocket support to Django.
- Daphne – ASGI server used to serve the Django application with real-time support.
- SimpleJWT – Implements JSON Web Token authentication for secure API access.
- SQLite – Lightweight database used for local development.
- Docker – Containerizes the application for consistent development and deployment environments


