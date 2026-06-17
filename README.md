# MiniTalk

MiniTalk is a lightweight social journaling web app where users can share thoughts, interact with others, and explore public posts.

## Features

- User authentication (login / register / logout)
- New accounts require admin approval before login
- Create and manage posts (public / private)
- Explore public posts from other users
- Comment system (AJAX, real-time update)
- User profiles with avatars and bio
- Follow / unfollow users
- AI-powered translation for posts (OpenAI API)
- Frontend caching for translations (reduces API calls and latency)

---

## Tech Stack

### Backend
- Python 3
- Django
- SQLite (development) / production-ready DB structure

### Frontend
- HTML / CSS
- JavaScript

### Deployment
- Gunicorn (WSGI server)
- Nginx (reverse proxy + static files)
- Ubuntu cloud server

### AI Integration
- OpenAI API (text translation)
- Prompt-based language detection and translation

---

## Setup (Local)

```bash
git clone https://github.com/Martha-LB/minitalk.git
cd minitalk

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export OPENAI_API_KEY="your-key"

python manage.py migrate
python manage.py runserver
```