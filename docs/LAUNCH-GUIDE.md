# 📣 Launch Guide — Posting This Project on LinkedIn

Everything needed to take this project public: what to fix first, how to capture
screenshots and video, the post script itself, and how to handle the replies.

> **Keep this private?** This file is committed like any other. If you'd rather it
> not appear in the public repo, add `docs/LAUNCH-GUIDE.md` to `.gitignore` before
> your next commit.

---

## ✅ Step 0 — Pre-flight (do this first)

These are the things that must be true before anyone clicks your link.

### 0.1 Rotate the production secrets on Render

The old `SECRET_KEY` was committed to this repo, so treat it as burned. Generate a new one:

```bash
cd backend
venv/Scripts/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then in **Render → smart-academic-backend → Environment**, set:

| Key | Value |
|---|---|
| `SECRET_KEY` | the freshly generated string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `smart-academic-dashboard-hi7g.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://smart-academic-frontend.onrender.com` |
| `DJANGO_SUPERUSER_PASSWORD` | a strong password you choose |

### 0.2 Change the admin password

`build.sh` used to create an admin with the password `Admin@1234`, which was published
in this repo. If that superuser exists on your live site, **anyone can log into
`/admin/` and read or delete your entire database right now.**

Log into `https://smart-academic-dashboard-hi7g.onrender.com/admin/` and change it,
or delete the user and let the updated `build.sh` recreate it from the env var above.

### 0.3 Redeploy and verify

After the deploy finishes, confirm both are still up:

- Frontend → https://smart-academic-frontend.onrender.com
- Admin → https://smart-academic-dashboard-hi7g.onrender.com/admin/

Then log in as `s6a01 / Student@1234` and click through every page. A broken demo is
worse than no demo.

---

## 🎬 Step 1 — Make the app look alive

**This matters more than anything else here.** The seeded database ships with
**zero attendance sessions and zero exams**, so every chart renders empty. Screenshots
of empty charts make the project look unfinished.

Spend 15 minutes generating real-looking data first:

1. Log in as **`prof_sharma / Faculty@1234`**
2. **Attendance → Mark Attendance** — record 8–10 sessions across different subjects and
   dates. Deliberately mark a few students absent repeatedly so the at-risk warnings and
   the red/green colour coding actually appear.
3. **Resources → Upload** — add 4–5 files across different subjects and types
   (Notes, Assignment, Reference, PYQ). Any small PDF works.
4. **Marks → Create Exam** — create 2–3 exams, then enter marks. Spread the scores so
   some students pass and some fail, and mark one or two absent.
5. Log in as **`hod_cs / HOD@1234`** and send a notice to all faculty.

Now the pie charts have slices, the bar charts have bars, the low-attendance banner
appears, and the notification bell has a red badge. *That* is what you screenshot.

---

## 📸 Step 2 — Screenshots

Save these four into `docs/screenshots/` using **exactly these filenames** — the README
already references them:

| Filename | Page | Log in as |
|---|---|---|
| `student-home.png` | Student → Home (charts + low-attendance banner) | `s6a01` |
| `faculty-attendance.png` | Faculty → Attendance → Mark Attendance | `prof_sharma` |
| `hod-home.png` | HOD → Home (department stats + pie chart) | `hod_cs` |
| `reports.png` | A downloaded Excel report open in Excel, or the PDF | `prof_sharma` |

### How to capture on Windows 11

**Snipping Tool** — press `Win + Shift + S`, drag over the area, then paste into Paint
and save as PNG. Simple and built in.

**Better: full-page browser capture.** In Chrome or Edge, press `F12` → `Ctrl + Shift + P`
→ type `screenshot` → choose **"Capture full size screenshot."** This grabs the entire
page including content below the fold, at proper resolution, with no browser chrome.

### Getting them to look good

- **Set your browser to 1920×1080 or use `Ctrl + -` to zoom to 80%** so more fits on screen
- **Hide your bookmarks bar** (`Ctrl + Shift + B`) and use an incognito window — no
  personal tabs, no extensions in shot
- **Take one mobile shot too.** `F12` → `Ctrl + Shift + M` → pick "iPhone 14 Pro" → capture
  the sidebar drawer open. Showing responsive design is a genuine differentiator
- **Crop out anything personal** — your name in the corner is fine, your other tabs are not

---

## 🎥 Step 3 — The video

A 30–60 second clip is the single highest-leverage thing in the post. LinkedIn pushes
native video far harder than link-only posts, and most people will never leave the feed.

### What to record

Follow one continuous story rather than clicking randomly:

| Time | Show |
|---|---|
| 0:00–0:08 | Login page → log in as faculty |
| 0:08–0:20 | Mark attendance — toggle a few students, hit save |
| 0:20–0:30 | Download the Excel report, open it so the colour coding is visible |
| 0:30–0:42 | Log out → log in as the student → the attendance you just marked appears |
| 0:42–0:55 | Student charts, low-attendance warning, recovery calculator |
| 0:55–1:00 | Quick flash of the HOD dashboard |

That arc shows the **data flowing between roles**, which is the actually impressive part
and what distinguishes this from a static UI mockup.

### Tools

- **Xbox Game Bar** — `Win + G`, built into Windows 11, records the active window
- **ShareX** (free, better) — records a selected region straight to MP4 or GIF
- **Clipchamp** — ships with Windows 11, good enough for trimming and captions

### Specs

- **MP4**, 1080p, under 60 seconds
- **Square (1:1) or vertical (4:5)** beats 16:9 — it occupies more of the mobile feed
- **Add text captions.** Most people watch on mute. Even simple labels like
  "Faculty marks attendance →" make it followable without sound
- No music needed

---

## ✍️ Step 4 — The post script

### Main version (recommended)

> Built a Smart Academic Dashboard — a full-stack portal that replaces the scattered
> systems colleges use for attendance, marks, and study material.
>
> Three roles, three different views of the same data:
>
> 🧑‍🎓 **Students** — attendance %, a recovery calculator that works out how many classes
> they need to get back above 75%, marks, and timetable
> 👨‍🏫 **Faculty** — mark attendance, upload resources, enter marks, export Excel/PDF reports
> 🏫 **HODs** — department-wide stats, at-risk student alerts, and a notice board
>
> **Stack:** Django REST Framework + React 19 + Tailwind, PostgreSQL, deployed on Render.
>
> Three things I learned the hard way:
>
> → **JWT refresh-token rotation.** Getting an Axios interceptor to catch a 401, refresh
> silently, and retry the original request — without infinite loops — took longer than
> the feature it protects.
> → **Server-side report generation.** Styled Excel with openpyxl (frozen headers,
> conditional colour coding) and landscape PDFs with reportlab.
> → **Role-based routing.** One login endpoint resolving to three entirely different
> dashboards, with route guards that hold up if someone types a URL directly.
>
> Built as my college major project. Live demo and full source below — genuinely open to
> feedback, especially on the API design.
>
> 🔗 Demo: https://smart-academic-frontend.onrender.com
> 💻 Code: https://github.com/AmanSaxena08/Smart-Academic-Dashboard
>
> *(Demo is on a free tier — first load takes ~40s to wake the server.)*
>
> #Django #React #FullStack #Python #WebDevelopment #OpenSource

### Shorter version

> Students can't see their attendance until it's too late to fix it. So I built
> something that tells them: "attend the next 6 classes and you're back above 75%."
>
> Smart Academic Dashboard — one portal, three roles:
> • Students track attendance, marks, resources, timetable
> • Faculty mark attendance and export Excel/PDF reports
> • HODs see the whole department and flag at-risk students
>
> Django REST + React 19 + PostgreSQL, deployed on Render.
>
> My college major project. Demo and code below — feedback welcome 👇
>
> 🔗 https://smart-academic-frontend.onrender.com
> 💻 https://github.com/AmanSaxena08/Smart-Academic-Dashboard
>
> #Django #React #Python #FullStack

### Why these work

- **They open with the problem, not "excited to announce."** The recovery calculator is
  the most interesting thing you built — lead with it.
- **They name specific technical difficulties.** "JWT rotation without infinite loops"
  invites a real conversation; "learned a lot" invites nothing.
- **They end with a question.** LinkedIn weights comments far above likes.
- **They're honest about scope.** "College major project" is accurate, and it protects
  you — nobody can accuse you of overselling.

---

## 📤 Step 5 — Posting mechanics

**Timing.** Tuesday–Thursday, 9–11 AM IST. Avoid Friday evening and weekends.

**Media.** Upload the video natively — never post a YouTube link as the primary media.
If you're only using stills, upload 3–4 images as a carousel rather than one.

**Links.** LinkedIn suppresses posts with external links in the body. Two options:
put the links in the first comment instead and write "links in comments," or keep them
in the body and accept slightly less reach. For a portfolio post, keeping them in the
body is usually worth it — reach matters less than the right person clicking through.

**Hashtags.** 3–5, at the end. More looks spammy.

**First hour matters most.** Reply to every comment quickly — early engagement drives
how widely it circulates. Don't post and disappear.

**Also do this:** add the project to your LinkedIn **Featured** section and under
**Projects** on your profile. The post disappears from feeds in two days; the profile
entry is permanent, and that's what recruiters actually browse.

---

## 💬 Step 6 — Answering the replies

Expect these. Have answers ready.

**"Why not WebSockets for notifications?"**
Polling every 30s was the pragmatic call for the scale involved — a few hundred users
on a free tier. Django Channels is the upgrade path and it's on the roadmap.

**"Why JWT in localStorage? That's XSS-vulnerable."**
Correct, and it's a real limitation — it's documented in the README's security notes.
`httpOnly` cookies are the stronger choice; localStorage kept the demo deployable as a
static frontend and a separate API. Own it rather than getting defensive; acknowledging
a tradeoff you understand reads far better than pretending it isn't one.

**"Is this used by a real college?"**
No — built as a major project with seeded demo data. Say so plainly.

**"Can I use this for my college?"**
It's MIT licensed, so yes. Good outcome — that's a genuine lead.

---

## 📋 Final checklist

Before you hit post:

- [ ] `SECRET_KEY` rotated, `DEBUG=False` on Render
- [ ] Admin password changed from `Admin@1234`
- [ ] Redeployed, both URLs verified working
- [ ] Demo data generated so charts aren't empty
- [ ] 4 screenshots saved into `docs/screenshots/`
- [ ] README renders correctly on GitHub (check the tables and images)
- [ ] Repo description and topics set on GitHub (`django`, `react`, `rest-api`, `education`)
- [ ] Video recorded, captioned, under 60s
- [ ] Logged in as all three roles one final time to confirm nothing is broken
- [ ] Post drafted, links tested by clicking them
