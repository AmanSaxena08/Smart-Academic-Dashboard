# 📤 Share Kit — Sending This Project to a Company

Copy-paste templates for sharing the project with a recruiter, hiring manager, or in a
job application.

---

## The one rule

**A reviewer gives you 60 seconds, and they will not clone your repo.**

So the order matters: *demo link first, repo second, explanation last.* Everything below
is built around that.

Demo credentials are already handled — the login page now has **one-click "View as
Student / Faculty / HOD" buttons**, so a reviewer never types anything. You should still
list the credentials in your message as a fallback, in case the buttons fail.

---

## ⚠️ Before you send: wake the server

The demo runs on Render's free tier and sleeps after ~15 minutes of inactivity. A cold
start takes **40–60 seconds**. If a recruiter clicks your link and sees a blank screen,
they close the tab and you never know it happened.

**Two options:**

**Quick fix** — open https://smart-academic-frontend.onrender.com yourself 2 minutes
before you send the message. The server stays awake for ~15 minutes after.

**Proper fix (10 minutes, do this once)** — set up a free uptime pinger so the server
never sleeps:

1. Go to [cron-job.org](https://cron-job.org) or [UptimeRobot](https://uptimerobot.com) — both free
2. Create a monitor hitting `https://smart-academic-dashboard-hi7g.onrender.com/admin/login/`
3. Set the interval to **every 14 minutes**

Now the demo is always instant. Worth doing before any application goes out.

---

## 📧 Template 1 — Email to a recruiter / hiring manager

> **Subject:** Full-stack developer application — Aman Saxena (live demo inside)
>
> Hi [Name],
>
> I'm applying for the [Role] position at [Company]. Rather than just describe my work,
> here's something you can click:
>
> **🔗 Live demo:** https://smart-academic-frontend.onrender.com
> **💻 Source:** https://github.com/AmanSaxena08/Smart-Academic-Dashboard
>
> It's a Smart Academic Dashboard — a role-based college portal where students track
> attendance and marks, faculty mark attendance and export Excel/PDF reports, and HODs
> oversee the department. The login page has **one-click demo buttons** for all three
> roles, so there's nothing to sign up for.
>
> The parts I'd point you to: JWT auth with silent token refresh, server-side Excel and
> PDF report generation, and role-based routing where one login endpoint resolves to
> three different dashboards.
>
> Built with Django REST Framework, React 19, and PostgreSQL, deployed on Render.
>
> Happy to walk through any part of the code.
>
> Best,
> Aman Saxena
> [phone] · [LinkedIn] · [GitHub]

---

## 💬 Template 2 — Short message (LinkedIn DM, WhatsApp, Slack)

> Hi [Name] — applying for [Role]. Here's a project you can click through in 2 minutes:
>
> 🔗 https://smart-academic-frontend.onrender.com
> (one-click demo logins on the page — Student / Faculty / HOD)
>
> 💻 https://github.com/AmanSaxena08/Smart-Academic-Dashboard
>
> Full-stack college portal — Django REST + React 19 + PostgreSQL. Attendance tracking,
> Excel/PDF report generation, JWT auth with role-based dashboards.
>
> (Demo is on a free tier — give it ~40s on first load.)

---

## 📄 Template 3 — Resume / CV line

> **Smart Academic Dashboard** — Full-stack role-based college portal
> *Django REST Framework, React 19, PostgreSQL, Tailwind, deployed on Render*
> Built a three-role portal (student/faculty/HOD) with JWT authentication and silent
> token refresh, server-side Excel and PDF report generation, and attendance analytics
> with automated at-risk detection. 7 Django apps, 40+ REST endpoints.
> `github.com/AmanSaxena08/Smart-Academic-Dashboard` · Live demo available

---

## 🗣 Template 4 — If they ask you to walk through it

A 3-minute structure that works in an interview:

1. **The problem** (20s) — "Students find out they're below 75% attendance when it's
   already too late to fix. Faculty track it in spreadsheets."
2. **The demo** (90s) — Log in as faculty → mark attendance → download the Excel report
   → log in as the student → the attendance appears, with a calculator telling them
   exactly how many classes to attend to recover.
3. **One technical deep-dive** (60s) — Pick the JWT refresh interceptor. Explain the
   401 → refresh → retry cycle and how you avoid infinite loops when the refresh itself
   fails.
4. **What you'd do differently** (30s) — "JWT in localStorage works for a demo but
   `httpOnly` cookies are the right call for production. Notifications poll every 30
   seconds; Channels would be better."

That last point matters more than people expect. Knowing the limits of your own work
is the clearest signal that you actually built it.

---

## ✅ Pre-send checklist

- [ ] Server woken up (or uptime pinger configured)
- [ ] Clicked all three demo buttons yourself — confirmed each lands on the right dashboard
- [ ] Demo data present so charts aren't empty
- [ ] Screenshots in the README (a reviewer may check the repo first)
- [ ] Repo is **public**, with description and topics set
- [ ] Links tested by pasting them into a fresh incognito window
- [ ] Your name and contact details are in the README
