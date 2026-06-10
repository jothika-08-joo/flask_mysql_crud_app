# ✅ MyTasker — Multi-User Task Manager

A full-stack **Flask + MySQL** task management web application with secure user authentication, session management, connection pooling, Docker containerisation, and CI/CD deployment on Render.

🌐 **Live Demo:** [tasker-app-94hb.onrender.com](https://tasker-app-94hb.onrender.com)  
📁 **GitHub:** [github.com/jothika-08-joo/flask_mysql_crud_app](https://github.com/jothika-08-joo/flask_mysql_crud_app)

---

## ✨ Features

- 🔐 **User Authentication** — Secure signup and login with password hashing using Werkzeug
- 👤 **Multi-User Support** — Each user sees and manages only their own tasks (data isolation)
- ✅ **Full CRUD** — Create, Read, Update, and Delete tasks
- 🏊 **Connection Pooling** — MySQL connection pool (pool size: 5) for efficient database handling
- 🛡️ **Custom Login Decorator** — `@login_required` protects all private routes
- 🌍 **Environment Variables** — Sensitive config stored in `.env`, never in code
- 🐳 **Docker** — Containerised with Docker and Docker Compose
- ⚙️ **CI/CD** — GitHub Actions pipeline for automated deployment
- ☁️ **Deployed** — Live on Render

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10, Flask 3.1.3 |
| Database | MySQL 8.0 |
| Auth | Werkzeug (password hashing + session) |
| Frontend | HTML, Bootstrap 5, Jinja2 |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## 🗄️ Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Todo table
CREATE TABLE todo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(20) NOT NULL,
    completed VARCHAR(20) DEFAULT 'pending',
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🔁 Application Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Redirects to task list |
| `/signup` | GET, POST | Register a new user |
| `/login` | GET, POST | Login existing user |
| `/logout` | GET, POST | Clear session and logout |
| `/add` | GET | Show add task form |
| `/add_tasks` | POST | Save new task to database |
| `/get_tasks` | GET | View all tasks for logged-in user |
| `/update/<id>` | GET | Show edit form for a task |
| `/update_tasks/<id>` | POST | Save updated task |
| `/delete_tasks/<id>` | POST | Delete a task |

---

## 📁 Project Structure

```
flask_mysql_crud_app/
├── app.py                  ← All backend logic (routes, DB, auth)
├── Dockerfile              ← Container build instructions
├── docker-compose.yml      ← Runs Flask + MySQL together
├── requirements.txt        ← Python dependencies
├── .env.example            ← Environment variable template
└── templates/
    ├── base.html           ← Navbar + layout (parent template)
    ├── signup.html         ← Registration page
    ├── login.html          ← Login page
    ├── add_tasks.html      ← Add task form
    ├── update_tasks.html   ← Edit task form
    └── view_tasks.html     ← Task dashboard
```

---

## 🚀 Getting Started

### Option 1 — Run with Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/jothika-08-joo/flask_mysql_crud_app.git
cd flask_mysql_crud_app

# 2. Create your .env file
cp .env.example .env
# Edit .env and fill in your values

# 3. Start both Flask app and MySQL together
docker-compose up --build
```

App will be running at `http://localhost:5000`

---

### Option 2 — Run Locally (Without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/jothika-08-joo/flask_mysql_crud_app.git
cd flask_mysql_crud_app

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your .env file
cp .env.example .env
# Edit .env with your MySQL credentials

# 5. Run the app
python app.py
```

---

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`:

```env
DB_HOST=your_host_name
DB_USER=your_user_name
DB_PASSWORD=your_password
DB_NAME=your_db_name
SECRET_KEY=your_secret_key_name
```

> ⚠️ Never commit your real `.env` file to GitHub. Only `.env.example` is committed.

---

## 🐳 Docker Setup

**Dockerfile** — builds the Flask app image:
- Base image: `python:3.10-slim`
- Working directory: `/app`
- Installs requirements, copies code, exposes port 5000
- Runs: `python app.py`

**docker-compose.yml** — runs two services:
- `db` — MySQL 8.0 with persistent volume (`db_data`)
- `app` — Flask app, connects to `db` service
- `depends_on` ensures MySQL starts before Flask

---

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** to automate deployment:

1. Every push to `main` branch triggers the pipeline
2. Builds and tests the application
3. Deploys automatically to Render on success

---

## 🔐 Security Features

- Passwords are **never stored as plain text** — hashed using `werkzeug.security.generate_password_hash`
- Login verified using `check_password_hash`
- All protected routes use a custom `@login_required` decorator
- Every task query filters by both `user_id` AND task `id` — users can never access each other's data
- Sensitive credentials stored in `.env`, excluded from version control

---

## 📸 Screenshots

### Login Page
![Login Page](https://github.com/jothika-08-joo/flask_mysql_crud_app/blob/c21fc529a456d4b6f24bb5c526bd27d18b757abb/login.png)

### Signup Page
![Signup Page](https://github.com/jothika-08-joo/flask_mysql_crud_app/blob/c21fc529a456d4b6f24bb5c526bd27d18b757abb/signup.png)

### Add Task
![Add Task](https://github.com/jothika-08-joo/flask_mysql_crud_app/blob/c21fc529a456d4b6f24bb5c526bd27d18b757abb/add_task.png)

### Get Task
![Get Task](https://github.com/jothika-08-joo/flask_mysql_crud_app/blob/c21fc529a456d4b6f24bb5c526bd27d18b757abb/get_tasks.png)

### Update Task
![Update Task](https://github.com/jothika-08-joo/flask_mysql_crud_app/blob/c21fc529a456d4b6f24bb5c526bd27d18b757abb/update_task.png)

## 🧑‍💻 Author

**Jothika K**  
B.Sc. Computer Science — Government Arts College (Autonomous), Salem  
- GitHub: [@jothika-08-joo](https://github.com/jothika-08-joo)  
- LinkedIn: [jothika-kumaravadivel](https://linkedin.com/in/jothika-kumaravadivel-591a1a2b2)  
- Email: jothikakumaravadivel@gmail.com  
- Live Project: [tasker-app-94hb.onrender.com](https://tasker-app-94hb.onrender.com)
