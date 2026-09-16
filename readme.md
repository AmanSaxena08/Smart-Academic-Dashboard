# 🎓 Smart Academic Dashboard

A full-stack web application that connects **students, faculty, and HODs** on a single portal for managing attendance, study resources, exam marks, timetables, and notices.

[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**🔗 [Live Demo](https://smart-academic-frontend.onrender.com)** · [Report a bug](https://github.com/AmanSaxena08/Smart-Academic-Dashboard/issues)

> ⏳ **Note:** the demo runs on Render's free tier, which sleeps after inactivity.
> The first request can take **40–60 seconds** to wake the server. It is not broken — give it a moment.

---

## 📸 Screenshots

| Student Dashboard | Faculty Attendance |
|:---:|:---:|
| ![Student dashboard](docs/screenshots/student-home.png) | ![Faculty attendance](docs/screenshots/faculty-attendance.png) |

| HOD Overview | Reports (Excel / PDF) |
|:---:|:---:|
| ![HOD overview](docs/screenshots/hod-home.png) | ![Reports](docs/screenshots/reports.png) |

---

## 🔑 Demo Credentials

Try the live demo with any of these accounts:

| Role | Username | Password |
|---|---|---|
| **Student** | `s6a01` | `Student@1234` |
| **Faculty** | `prof_sharma` | `Faculty@1234` |
| **HOD** | `hod_cs` | `HOD@1234` |

Other seeded accounts: students follow the pattern `s{semester}{section}{number}` (e.g. `s6b05`), and faculty include `prof_gupta`, `prof_verma`, `prof_singh`.

---

## 📖 Overview

Smart Academic Dashboard replaces scattered college systems with one portal. A single login page routes each user to the right dashboard based on their role.

- **Students** view attendance, download study material, check results, and track their timetable
- **Faculty** mark attendance, upload resources, publish marks, and export reports
- **HODs** oversee the department — students, faculty, attendance, results — and send notices

**Highlights**

- Single login with automatic role-based redirection
- Student self-registration with live password-strength validation
- Real-time notifications when resources or marks are published
- HOD notice board — broadcast to all faculty or specific members
- Downloadable **Excel** attendance reports and **PDF** marks reports
- Low-attendance warnings for students below 75%, with a recovery calculator
- Fully responsive — desktop, tablet, and mobile

---

## 🛠 Tech Stack

### Backend

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12+ | Language |
| Django | 5.2 | Web framework |
| Django REST Framework | 3.15.2 | REST API layer |
| simplejwt | 5.3.1 | JWT authentication |
| django-cors-headers | 4.6.0 | Cross-origin requests |
| Pillow | 11.2+ | Image / file handling |
| openpyxl | 3.1.5 | Excel report generation |
| reportlab | 4.2.5 | PDF report generation |
| django-jazzmin | 2.6.0 | Admin panel theme |
| PostgreSQL / SQLite | — | Database (prod / dev) |

### Frontend

| Technology | Version | Purpose |
|---|---|---|
| React | 19 | UI framework |
| Vite | 7 | Build tool |
| Tailwind CSS | 4 | Styling |
| React Router | 7 | Client-side routing |
| Axios | 1.x | HTTP client + JWT interceptors |
| Recharts | 3.x | Charts and graphs |
| Lucide React | 0.577 | Icon library |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm 9+

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data        # optional: 120 demo students, faculty, subjects
python manage.py createsuperuser  # for the /admin/ panel
python manage.py runserver
```

Backend runs at **http://127.0.0.1:8000/**

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:5173/**

### Configuration

The frontend defaults to `http://127.0.0.1:8000/api`. To point it elsewhere (for example if port 8000 is already taken), create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8001/api
```

The backend reads these environment variables — all optional in development:

| Variable | Default (dev) | Purpose |
|---|---|---|
| `SECRET_KEY` | insecure dev key | **Required when `DEBUG=False`** |
| `DEBUG` | `True` | Set `False` in production |
| `DATABASE_URL` | SQLite file | Postgres connection string |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,.onrender.com` | Comma-separated hosts |
| `CORS_ALLOWED_ORIGINS` | frontend Render URL | Comma-separated origins |
| `DJANGO_SUPERUSER_PASSWORD` | *unset* | If set, `build.sh` creates an admin |
| `SEED_DEMO_DATA` | `true` | Run `seed_data` during deploy |

---

## 👥 User Roles

| Role | Theme | Access | Account Creation |
|---|---|---|---|
| Super Admin | — | Django admin panel | `python manage.py createsuperuser` |
| Student | Indigo | Student dashboard | Self-registration at `/register` |
| Faculty | Emerald | Faculty dashboard | Created by Super Admin |
| HOD | Amber | HOD dashboard | Faculty with `is_hod=True` |

### HOD Year Groups

HODs are assigned year groups via boolean fields on `FacultyProfile`. A HOD can hold several at once.

| Field | Manages |
|---|---|
| `hod_year_1` | Semesters 1 & 2 |
| `hod_year_2` | Semesters 3 & 4 |
| `hod_year_3` | Semesters 5 & 6 |
| `hod_year_4` | Semesters 7 & 8 |

### Login Redirect Logic

```js
if (role === "student")           // → /student/home
if (role === "faculty" && is_hod) // → /hod/home
if (role === "faculty" && !is_hod)// → /faculty/home
```

---

## ✨ Features

### 🔐 Authentication

- Single login page for all roles
- JWT — 8-hour access token, 7-day refresh token, rotation enabled
- Automatic token refresh via an Axios interceptor on `401`
- Role-based protected routes
- Two-step student registration with a live password-strength meter

Password rules: minimum 8 characters, at least one uppercase, one lowercase, one number, and one special character.

### 🧑‍🎓 Student Dashboard

| Page | What it does |
|---|---|
| **Home** | Summary cards, pie chart (present vs absent), bar chart (subject-wise), low-attendance alert, recent resources and results |
| **Attendance** | Subject-wise cards with progress bars, dual-colour bar chart (green ≥75%, red <75%), history table, subject/date filters, **recovery calculator** |
| **Resources** | Files grouped by subject, filter by type, search by title, download (marks as viewed) |
| **Marks** | Summary cards, performance bar chart with pass/fail colouring, grouped by subject |
| **Timetable** | Week view across 6 days, today view, today highlighted with a pulsing dot |
| **Profile** | Academic info, edit personal details, change password |

### 👨‍🏫 Faculty Dashboard

| Page | What it does |
|---|---|
| **Home** | Lectures conducted, resources shared, exams created, bar chart of lectures per subject |
| **Attendance** | Mark attendance (click to toggle, Mark All, live counters), session history, **Excel export** with filters |
| **Resources** | Upload with title/description/type, manage with inline edit and delete |
| **Marks** | Create exams, enter per-student marks with absent flag and remarks, **PDF export** |
| **Timetable** | Week and today views with a subject colour legend |
| **Students** | Per-section list with attendance %, at-risk badges, expandable subject breakdown |
| **Notice Board** | Notices from HOD, unread indicator, auto-marks read on expand |
| **Profile** | Faculty info, edit details, change password |

### 🏫 HOD Dashboard

| Page | What it does |
|---|---|
| **Home** | Department-wide stats, pie chart (safe vs at-risk), quick averages |
| **Students** | All students in the HOD's year groups, filters, at-risk badges |
| **Faculty** | All faculty with expandable subject lists |
| **Attendance** | Section-wise view with colour-coded bars (green ≥75%, yellow 60–75%, red <75%) |
| **Exams** | All exam results with appeared/passed counts and pass % |
| **Notice Board** | Create notices for all or specific faculty, view and delete sent notices |
| **Profile** | HOD info, year-group badges, edit details |

### 🔔 Notifications

Available in all three dashboards. Red badge with unread count, dropdown of the last 20, icons by type, relative timestamps, mark-one/mark-all read, polling every 30 seconds.

Auto-created when:

- Faculty uploads a resource → enrolled students notified
- Faculty enters marks → that student notified
- HOD sends a notice → recipient faculty notified

---

## 🗄 Database Models

### `users`

| Model | Key fields |
|---|---|
| `CustomUser` | extends `AbstractUser` — role, phone, profile_pic |
| `StudentProfile` | enrollment_number, branch, semester, section, date_of_birth, address |
| `FacultyProfile` | employee_id, department, designation, joining_date, is_hod, hod_year_1…4 |

### `academics`

| Model | Key fields |
|---|---|
| `Department` | name, code |
| `Subject` | name, code, semester, department, faculty, credits |
| `Section` | name, semester, department, students (M2M) |
| `Timetable` | section, subject, day, start_time, end_time |

### `attendance`

| Model | Key fields |
|---|---|
| `AttendanceSession` | faculty, subject, section, date, start_time, topic_covered — unique on (subject, section, date, start_time) |
| `AttendanceRecord` | session, student, status — unique on (session, student) |

### `resources`

| Model | Key fields |
|---|---|
| `Resource` | title, description, resource_type, file, subject, section, uploaded_by, is_active |
| `ResourceView` | resource, student, viewed_at — unique on (resource, student) |

### `exams`

| Model | Key fields |
|---|---|
| `Exam` | title, exam_type, subject, section, conducted_by, date, max_marks, passing_marks |
| `ExamResult` | exam, student, marks_obtained, is_absent, remarks — unique on (exam, student) |

### `notifications` / `notices`

| Model | Key fields |
|---|---|
| `Notification` | recipient, title, message, notification_type, is_read, created_at |
| `Notice` | title, content, sent_by, recipient_type, specific_recipients (M2M), is_active |
| `NoticeRead` | notice, faculty, read_at — unique on (notice, faculty) |

---

## 🔌 API Endpoints

### Users — `/api/users/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/register/` | Student registration | No |
| POST | `/login/` | Login — returns JWT + user data | No |
| POST | `/token/refresh/` | Refresh access token | No |
| GET | `/profile/` | Get full profile | Yes |
| PUT | `/profile/update/` | Update personal info | Yes |
| POST | `/change-password/` | Change password | Yes |
| GET | `/hod/overview/` | Department overview stats | HOD |
| GET | `/hod/students/` | Students in HOD's year groups | HOD |
| GET | `/hod/faculty/` | Faculty in HOD's year groups | HOD |
| GET | `/hod/attendance/` | Section-wise attendance overview | HOD |
| GET | `/hod/exams/` | All exams in HOD's year groups | HOD |

### Academics — `/api/academics/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/departments/` | List departments | Yes |
| GET | `/subjects/` | List subjects by role | Yes |
| GET | `/sections/` | List all sections | Yes |
| GET | `/student-timetable/` | Student's timetable | Student |
| GET | `/faculty-timetable/` | Faculty's timetable | Faculty |

### Attendance — `/api/attendance/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/create-session/` | Mark attendance | Faculty |
| GET | `/section-students/` | Students in a section | Faculty |
| GET / PUT | `/session/<id>/` | View or update a session | Faculty |
| GET | `/faculty-sessions/` | Faculty's sessions | Faculty |
| GET | `/my-summary/` | Student attendance summary | Student |
| GET | `/my-detail/` | Student attendance history | Student |
| GET | `/students-summary/` | All students' attendance | Faculty |
| GET | `/download-excel/` | Download Excel report | Faculty |

### Resources — `/api/resources/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/upload/` | Upload a resource | Faculty |
| GET | `/faculty/` | Faculty's resources | Faculty |
| GET / PUT / DELETE | `/<id>/` | View, edit, or delete | Faculty |
| GET | `/student/` | Student's resources | Student |
| POST | `/<id>/viewed/` | Mark as viewed | Student |

### Exams — `/api/exams/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/create/` | Create an exam | Faculty |
| GET / PUT / DELETE | `/<id>/` | View, edit, or delete | Faculty |
| POST | `/<id>/results/` | Enter marks | Faculty |
| GET | `/faculty/` | Faculty's exams | Faculty |
| GET | `/my-results/` | Student's results | Student |
| GET | `/my-summary/` | Student's exam summary | Student |
| GET | `/download-pdf/` | Download PDF report | Faculty |

### Notifications — `/api/notifications/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/` | Notifications + unread count | Yes |
| PUT | `/<id>/read/` | Mark as read | Yes |
| PUT | `/mark-all-read/` | Mark all as read | Yes |

### Notices — `/api/notices/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/create/` | Create a notice | HOD |
| GET | `/hod/` | HOD's sent notices | HOD |
| DELETE | `/<id>/delete/` | Delete a notice | HOD |
| GET | `/faculty/` | Faculty's received notices | Faculty |
| PUT | `/<id>/read/` | Mark notice as read | Faculty |

---

## 📁 Project Structure

```
Smart-Academic-Dashboard/
│
├── backend/
│   ├── core/              ← Django project (settings, urls, wsgi)
│   ├── users/             ← CustomUser, profiles, HOD views
│   ├── academics/         ← Department, Subject, Section, Timetable
│   ├── attendance/        ← Sessions, records, Excel export
│   ├── resources/         ← Resource uploads and views
│   ├── exams/             ← Exams, results, PDF export
│   ├── notifications/     ← Bell notifications
│   ├── notices/           ← HOD notice board
│   ├── build.sh           ← Render build script
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── api/axios.js            ← JWT interceptors + auto refresh
│       ├── context/AuthContext.jsx ← Global auth state
│       ├── routes/                 ← Role-based route protection
│       ├── components/shared/      ← Layouts + notification bell
│       └── pages/                  ← auth / student / faculty / hod
│
├── docs/screenshots/
├── render.yaml
└── LICENSE
```

---

## 🌐 Deployment

Deployed on [Render](https://render.com) via `render.yaml` — a Python web service for the backend and a static site for the frontend.

**Required environment variables in production:**

```env
SECRET_KEY=<generate a fresh one>
DEBUG=False
DATABASE_URL=<postgres connection string>
ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com
```

The frontend needs `VITE_API_URL` set to the backend's `/api` URL at build time.

> The app **refuses to start** with `DEBUG=False` and no `SECRET_KEY`, by design — it should never fall back to a key committed to source control.

---

## 🔒 Security Notes

- `SECRET_KEY` is read from the environment; there is no production fallback
- `CORS_ALLOW_ALL_ORIGINS` is enabled only when `DEBUG=True`
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` are environment-driven
- `build.sh` creates a superuser only when `DJANGO_SUPERUSER_PASSWORD` is supplied
- JWT tokens are stored in `localStorage` — acceptable for a demo, though `httpOnly` cookies are the stronger production choice
- Uploaded files are stored on local disk — use object storage (S3 / Cloudinary) at scale

---

## 🧩 Known Limitations

- Notifications poll every 30 seconds rather than using WebSockets
- No email verification or password reset by email
- Uploaded media is not persisted across Render free-tier restarts
- `Pillow` and `psycopg2-binary` need recent versions on Python 3.13+; `psycopg2-binary` is skipped on Windows, since local development uses SQLite

---

## 🚀 Future Enhancements

- WebSocket notifications via Django Channels
- Assignment submission and grading
- Email alerts for low attendance
- Dark mode
- Cloud storage for uploaded files

---

## 📄 License

Released under the [MIT License](LICENSE).

---

Built by **[Aman Saxena](https://github.com/AmanSaxena08)** as a college major project.
