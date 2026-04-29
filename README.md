# MiniTalk

MiniTalk is a lightweight social journaling web app where users can share thoughts, interact with others, and explore public posts.


## Features

- User authentication (login / register / logout)
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

## Key Technical Highlights

### 1. Asynchronous Interaction (AJAX)
- Comments are submitted via `fetch()` without page reload
- Real-time UI updates improve user experience

### 2. AI Translation Feature
- Integrated OpenAI API for dynamic text translation
- Prompt engineering for bilingual translation (EN ↔ ZH)

### 3. Frontend Caching Optimization
- Translations are cached in browser memory
- Avoids repeated API calls → reduces cost and latency

### 4. Production Deployment
- Full deployment with:
  - Gunicorn
  - Nginx
  - Static file handling via `collectstatic`
- Solved real-world issues like:
  - static file caching
  - environment variables for API keys
  - service configuration (systemd)

---

## Setup (Local)

```bash
git clone https://github.com/your-username/minitalk.git
cd minitalk

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export OPENAI_API_KEY="your-key"

python manage.py migrate
python manage.py runserver
```