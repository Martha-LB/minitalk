# MiniTalk

MiniTalk is a lightweight social journaling web application built with Django.  
Users can write personal posts, manage private entries, and explore content shared by others.

The project focuses on building a clean and functional full-stack application with user interaction features.


## Features

- User authentication (register, login, logout)
- Create, edit, and delete posts
- Public and private post visibility
- Personal post history
- Comment system with user interaction
- User profiles with avatar and bio
- Follow / unfollow users
- View other users' public profiles
- Clean UI with responsive layout


## Tech Stack

- Python 3
- Django
- SQLite
- Gunicorn
- Nginx


## Installation

1. Clone the repository:

```bash
git clone https://github.com/Martha-LB/minitalk.git
cd minitalk
```

2. Create a virtual environment

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
```