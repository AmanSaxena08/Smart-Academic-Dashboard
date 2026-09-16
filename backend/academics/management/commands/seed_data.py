from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from academics.models import Department, Subject, Section, Timetable
from users.models import StudentProfile, FacultyProfile
from attendance.models import AttendanceSession, AttendanceRecord
from exams.models import Exam, ExamResult
from resources.models import Resource
from notices.models import Notice
from notifications.models import Notification
from datetime import date, timedelta, time as dtime
from decimal import Decimal
import io as _io
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with complete college data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Starting data seeding...')

        # ── Department ────────────────────────────────────────
        dept, _ = Department.objects.get_or_create(
            name='Computer Science',
            defaults={'code': 'CS'}
        )
        self.stdout.write('✅ Department created')

        # ── Faculty ───────────────────────────────────────────
        faculty_data = [
            {'username': 'prof_sharma', 'first_name': 'Rajesh', 'last_name': 'Sharma', 'email': 'sharma@college.edu', 'emp_id': 'EMP001', 'designation': 'Associate Professor'},
            {'username': 'prof_gupta', 'first_name': 'Priya', 'last_name': 'Gupta', 'email': 'gupta@college.edu', 'emp_id': 'EMP002', 'designation': 'Assistant Professor'},
            {'username': 'prof_verma', 'first_name': 'Amit', 'last_name': 'Verma', 'email': 'verma@college.edu', 'emp_id': 'EMP003', 'designation': 'Professor'},
            {'username': 'prof_singh', 'first_name': 'Neha', 'last_name': 'Singh', 'email': 'singh@college.edu', 'emp_id': 'EMP004', 'designation': 'Assistant Professor'},
        ]

        faculty_users = []
        for f in faculty_data:
            user, created = User.objects.get_or_create(
                username=f['username'],
                defaults={
                    'first_name': f['first_name'],
                    'last_name': f['last_name'],
                    'email': f['email'],
                    'role': 'faculty'
                }
            )
            if created:
                user.set_password('Faculty@1234')
                user.save()
            FacultyProfile.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': f['emp_id'],
                    'department': 'Computer Science',
                    'designation': f['designation'],
                }
            )
            faculty_users.append(user)
        self.stdout.write('✅ Faculty created')

        # ── HOD ───────────────────────────────────────────────
        hod, created = User.objects.get_or_create(
            username='hod_cs',
            defaults={
                'first_name': 'Dr. Sunita',
                'last_name': 'Agarwal',
                'email': 'hod@college.edu',
                'role': 'faculty'
            }
        )
        if created:
            hod.set_password('HOD@1234')
            hod.save()
        FacultyProfile.objects.get_or_create(
            user=hod,
            defaults={
                'employee_id': 'HOD001',
                'department': 'Computer Science',
                'designation': 'Head of Department',
                'is_hod': True,
                'hod_year_3': True,
                'hod_year_4': True,
            }
        )
        self.stdout.write('✅ HOD created')

        # ── Subjects ──────────────────────────────────────────
        subjects_data = [
            # 5th Semester
            {'name': 'Data Structures', 'code': 'CS501', 'semester': 5, 'faculty': faculty_users[0]},
            {'name': 'Computer Networks', 'code': 'CS502', 'semester': 5, 'faculty': faculty_users[1]},
            {'name': 'Operating Systems', 'code': 'CS503', 'semester': 5, 'faculty': faculty_users[2]},
            {'name': 'Database Management', 'code': 'CS504', 'semester': 5, 'faculty': faculty_users[3]},
            {'name': 'Software Engineering', 'code': 'CS505', 'semester': 5, 'faculty': faculty_users[0]},
            # 6th Semester
            {'name': 'Artificial Intelligence', 'code': 'CS601', 'semester': 6, 'faculty': faculty_users[1]},
            {'name': 'Machine Learning', 'code': 'CS602', 'semester': 6, 'faculty': faculty_users[2]},
            {'name': 'Web Technologies', 'code': 'CS603', 'semester': 6, 'faculty': faculty_users[3]},
            {'name': 'Cloud Computing', 'code': 'CS604', 'semester': 6, 'faculty': faculty_users[0]},
            {'name': 'Cyber Security', 'code': 'CS605', 'semester': 6, 'faculty': faculty_users[1]},
            # 7th Semester
            {'name': 'Deep Learning', 'code': 'CS701', 'semester': 7, 'faculty': faculty_users[2]},
            {'name': 'Big Data Analytics', 'code': 'CS702', 'semester': 7, 'faculty': faculty_users[3]},
            {'name': 'Mobile Computing', 'code': 'CS703', 'semester': 7, 'faculty': faculty_users[0]},
            {'name': 'IoT Systems', 'code': 'CS704', 'semester': 7, 'faculty': faculty_users[1]},
            # 8th Semester
            {'name': 'Project Management', 'code': 'CS801', 'semester': 8, 'faculty': faculty_users[2]},
            {'name': 'Blockchain Technology', 'code': 'CS802', 'semester': 8, 'faculty': faculty_users[3]},
            {'name': 'Natural Language Processing', 'code': 'CS803', 'semester': 8, 'faculty': faculty_users[0]},
        ]

        subject_objects = {}
        for s in subjects_data:
            subj, _ = Subject.objects.get_or_create(
                code=s['code'],
                defaults={
                    'name': s['name'],
                    'semester': s['semester'],
                    'department': dept,
                    'faculty': s['faculty'],
                    'credits': 4,
                }
            )
            subject_objects[s['code']] = subj
        self.stdout.write('✅ Subjects created')

        # ── Sections ──────────────────────────────────────────
        sections_config = [
            {'name': 'A', 'semester': 5},
            {'name': 'B', 'semester': 5},
            {'name': 'A', 'semester': 6},
            {'name': 'B', 'semester': 6},
            {'name': 'A', 'semester': 7},
            {'name': 'B', 'semester': 7},
            {'name': 'A', 'semester': 8},
            {'name': 'B', 'semester': 8},
        ]

        section_objects = {}
        for sc in sections_config:
            sec, _ = Section.objects.get_or_create(
                name=sc['name'],
                semester=sc['semester'],
                department=dept
            )
            section_objects[f"{sc['semester']}{sc['name']}"] = sec
        self.stdout.write('✅ Sections created')

        # ── Students ──────────────────────────────────────────
        student_names = [
            ('Aarav', 'Sharma'), ('Bhavya', 'Patel'), ('Chirag', 'Gupta'),
            ('Divya', 'Singh'), ('Eshan', 'Verma'), ('Fatima', 'Khan'),
            ('Gaurav', 'Joshi'), ('Hema', 'Yadav'), ('Ishaan', 'Mehta'),
            ('Jaya', 'Agarwal'), ('Karan', 'Saxena'), ('Lakshmi', 'Nair'),
            ('Manav', 'Tiwari'), ('Nisha', 'Rajput'), ('Om', 'Pandey'),
        ]

        sem_section_combos = [
            (5, 'A'), (5, 'B'),
            (6, 'A'), (6, 'B'),
            (7, 'A'), (7, 'B'),
            (8, 'A'), (8, 'B'),
        ]

        student_count = 0
        for sem, sec_name in sem_section_combos:
            section = section_objects[f"{sem}{sec_name}"]
            for i, (first, last) in enumerate(student_names):
                username = f"s{sem}{sec_name.lower()}{i+1:02d}"
                enroll = f"CS{sem}{'A' if sec_name=='A' else 'B'}{i+1:03d}"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': first,
                        'last_name': last,
                        'email': f"{username}@student.edu",
                        'role': 'student'
                    }
                )
                if created:
                    user.set_password('Student@1234')
                    user.save()

                StudentProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'enrollment_number': enroll,
                        'branch': 'Computer Science',
                        'semester': sem,
                        'section': sec_name,
                    }
                )
                section.students.add(user)
                student_count += 1

        self.stdout.write(f'✅ {student_count} Students created')

        # ── Timetable ─────────────────────────────────────────
        timetable_data = [
            # Semester 5
            ('CS501', '5A', 'monday', '09:00', '10:00'),
            ('CS502', '5A', 'monday', '11:00', '12:00'),
            ('CS503', '5A', 'tuesday', '09:00', '10:00'),
            ('CS504', '5A', 'tuesday', '11:00', '12:00'),
            ('CS505', '5A', 'wednesday', '09:00', '10:00'),
            ('CS501', '5A', 'thursday', '09:00', '10:00'),
            ('CS502', '5A', 'friday', '09:00', '10:00'),
            ('CS503', '5A', 'friday', '11:00', '12:00'),
            ('CS501', '5B', 'monday', '10:00', '11:00'),
            ('CS502', '5B', 'tuesday', '10:00', '11:00'),
            ('CS503', '5B', 'wednesday', '10:00', '11:00'),
            ('CS504', '5B', 'thursday', '10:00', '11:00'),
            ('CS505', '5B', 'friday', '10:00', '11:00'),
            # Semester 6
            ('CS601', '6A', 'monday', '09:00', '10:00'),
            ('CS602', '6A', 'monday', '11:00', '12:00'),
            ('CS603', '6A', 'tuesday', '09:00', '10:00'),
            ('CS604', '6A', 'wednesday', '09:00', '10:00'),
            ('CS605', '6A', 'thursday', '09:00', '10:00'),
            ('CS601', '6A', 'friday', '09:00', '10:00'),
            ('CS601', '6B', 'monday', '10:00', '11:00'),
            ('CS602', '6B', 'tuesday', '10:00', '11:00'),
            ('CS603', '6B', 'wednesday', '10:00', '11:00'),
            ('CS604', '6B', 'thursday', '10:00', '11:00'),
            ('CS605', '6B', 'friday', '10:00', '11:00'),
            # Semester 7
            ('CS701', '7A', 'monday', '09:00', '10:00'),
            ('CS702', '7A', 'tuesday', '09:00', '10:00'),
            ('CS703', '7A', 'wednesday', '09:00', '10:00'),
            ('CS704', '7A', 'thursday', '09:00', '10:00'),
            ('CS701', '7A', 'friday', '09:00', '10:00'),
            ('CS701', '7B', 'monday', '10:00', '11:00'),
            ('CS702', '7B', 'tuesday', '10:00', '11:00'),
            ('CS703', '7B', 'wednesday', '10:00', '11:00'),
            ('CS704', '7B', 'friday', '10:00', '11:00'),
            # Semester 8
            ('CS801', '8A', 'monday', '09:00', '10:00'),
            ('CS802', '8A', 'tuesday', '09:00', '10:00'),
            ('CS803', '8A', 'wednesday', '09:00', '10:00'),
            ('CS801', '8A', 'thursday', '09:00', '10:00'),
            ('CS801', '8B', 'monday', '10:00', '11:00'),
            ('CS802', '8B', 'tuesday', '10:00', '11:00'),
            ('CS803', '8B', 'wednesday', '10:00', '11:00'),
        ]

        for code, sec_key, day, start, end in timetable_data:
            subj = subject_objects.get(code)
            sec = section_objects.get(sec_key)
            if subj and sec:
                Timetable.objects.get_or_create(
                    section=sec,
                    subject=subj,
                    day=day,
                    start_time=start,
                    defaults={'end_time': end}
                )
        self.stdout.write('✅ Timetable created')

        # ── Activity data ─────────────────────────────────────
        # Attendance, exams, resources and notices. Without these every
        # chart in the app renders empty, so a fresh deployment looks
        # unfinished. Guarded on AttendanceSession so redeploys are cheap
        # and this never double-seeds.
        if AttendanceSession.objects.exists():
            self.stdout.write('⏭  Activity data already present — skipping')
        else:
            rng = random.Random(20260916)  # deterministic between runs

            all_subjects = list(Subject.objects.select_related('faculty'))
            sections_by_sem = {}
            for sec in Section.objects.all():
                sections_by_sem.setdefault(sec.semester, []).append(sec)

            # Give each student a baseline reliability. The tail below 0.75
            # is what makes the low-attendance warnings and at-risk badges
            # visible in the UI.
            reliability = {}
            for stu in User.objects.filter(role='student'):
                roll = rng.random()
                if roll < 0.18:
                    reliability[stu.id] = rng.uniform(0.45, 0.72)   # at risk
                elif roll < 0.35:
                    reliability[stu.id] = rng.uniform(0.75, 0.85)   # borderline
                else:
                    reliability[stu.id] = rng.uniform(0.86, 0.99)   # healthy

            # ── Attendance ────────────────────────────────────
            today = date.today()
            weekdays = []
            probe = today - timedelta(days=1)
            while len(weekdays) < 45:
                if probe.weekday() < 5:          # Mon–Fri only
                    weekdays.append(probe)
                probe -= timedelta(days=1)
            weekdays.reverse()

            sessions, records = [], []
            topics = ['Introduction', 'Core Concepts', 'Case Study', 'Problem Solving',
                      'Lab Walkthrough', 'Revision', 'Advanced Topics', 'Group Discussion',
                      'Applications', 'Doubt Session', 'Recap', 'Assessment Prep']

            for idx, subj in enumerate(all_subjects):
                for sec in sections_by_sem.get(subj.semester, []):
                    students = list(sec.students.filter(role='student'))
                    if not students:
                        continue
                    slots = rng.sample(weekdays, min(10, len(weekdays)))
                    for n, day in enumerate(sorted(slots)):
                        sessions.append(AttendanceSession(
                            faculty=subj.faculty,
                            subject=subj,
                            section=sec,
                            date=day,
                            start_time=dtime(9 + (idx % 6), 0),
                            topic_covered=f"{topics[n % len(topics)]} — {subj.name}",
                        ))
            AttendanceSession.objects.bulk_create(sessions, batch_size=500)

            roster = {
                sec.id: list(sec.students.filter(role='student'))
                for sec in Section.objects.prefetch_related('students')
            }
            for sess in AttendanceSession.objects.all():
                for stu in roster.get(sess.section_id, []):
                    present = rng.random() < reliability.get(stu.id, 0.85)
                    records.append(AttendanceRecord(
                        session=sess, student=stu,
                        status='present' if present else 'absent',
                    ))
            AttendanceRecord.objects.bulk_create(records, batch_size=1000)
            self.stdout.write(
                f'✅ {len(sessions)} attendance sessions, {len(records)} records')

            # ── Exams and results ─────────────────────────────
            exam_plan = [
                ('Sessional 1', 'sessional1', Decimal('30'), Decimal('12'), 40),
                ('Sessional 2', 'sessional2', Decimal('30'), Decimal('12'), 12),
            ]
            exams, results = [], []
            for subj in all_subjects:
                for sec in sections_by_sem.get(subj.semester, []):
                    if not sec.students.exists():
                        continue
                    for title, etype, maxm, passm, days_ago in exam_plan:
                        exams.append(Exam(
                            title=f"{title} — {subj.name}",
                            exam_type=etype,
                            subject=subj,
                            section=sec,
                            conducted_by=subj.faculty,
                            date=today - timedelta(days=days_ago),
                            max_marks=maxm,
                            passing_marks=passm,
                        ))
            Exam.objects.bulk_create(exams, batch_size=500)

            for exam in Exam.objects.all():
                for stu in roster.get(exam.section_id, []):
                    if rng.random() < 0.04:
                        results.append(ExamResult(
                            exam=exam, student=stu, marks_obtained=Decimal('0'),
                            is_absent=True, remarks='Absent',
                            entered_by_id=exam.conducted_by_id))
                        continue
                    # Marks loosely track the student's engagement level.
                    base = reliability.get(stu.id, 0.85)
                    frac = min(0.99, max(0.15, rng.gauss(base * 0.88, 0.14)))
                    marks = Decimal(str(round(float(exam.max_marks) * frac, 1)))
                    passed = marks >= exam.passing_marks
                    results.append(ExamResult(
                        exam=exam, student=stu, marks_obtained=marks, is_absent=False,
                        remarks='Good' if frac > 0.75 else ('Pass' if passed else 'Needs improvement'),
                        entered_by_id=exam.conducted_by_id))
            ExamResult.objects.bulk_create(results, batch_size=1000)
            self.stdout.write(f'✅ {len(exams)} exams, {len(results)} results')

            # ── Resources ─────────────────────────────────────
            # One real PDF generated once and reused, so downloads in the
            # demo actually open instead of returning a broken file.
            try:
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import A4
                buf = _io.BytesIO()
                pdf = canvas.Canvas(buf, pagesize=A4)
                pdf.setFont('Helvetica-Bold', 16)
                pdf.drawString(72, 760, 'Smart Academic Dashboard')
                pdf.setFont('Helvetica', 11)
                pdf.drawString(72, 735, 'Sample study material for the demo deployment.')
                pdf.drawString(72, 715, 'Replace with real course content in production.')
                pdf.showPage()
                pdf.save()
                pdf_bytes = buf.getvalue()
            except Exception:
                pdf_bytes = b'Sample study material for the Smart Academic Dashboard demo.\n'

            res_plan = [
                ('Unit 1 — Lecture Notes', 'notes', 'Complete notes covering the first unit.'),
                ('Assignment 1', 'assignment', 'Submit before the next sessional.'),
                ('Previous Year Paper', 'pyq', 'Last year question paper for practice.'),
            ]
            made = 0
            for subj in all_subjects:
                for title, rtype, desc in res_plan:
                    r = Resource(
                        title=f"{title} — {subj.code}",
                        description=desc,
                        resource_type=rtype,
                        subject=subj,
                        uploaded_by=subj.faculty,
                    )
                    fname = f"{subj.code.lower()}_{rtype}.pdf"
                    r.file.save(fname, ContentFile(pdf_bytes), save=False)
                    r.save()
                    made += 1
            self.stdout.write(f'✅ {made} resources')

            # ── Notices from the HOD ──────────────────────────
            notice_plan = [
                ('Sessional 2 Schedule Released',
                 'The Sessional 2 timetable has been published. Please ensure syllabus '
                 'coverage is complete and share the marking scheme with your sections.'),
                ('Attendance Below 75% — Action Required',
                 'Several students have fallen below the 75% attendance threshold. '
                 'Kindly counsel the students in your sections and update their records.'),
                ('Department Meeting — Friday 3 PM',
                 'All faculty members are requested to attend the monthly department '
                 'review meeting in the seminar hall.'),
            ]
            faculty_all = list(User.objects.filter(role='faculty').exclude(id=hod.id))
            for title, body in notice_plan:
                notice = Notice.objects.create(
                    title=title, content=body, sent_by=hod, recipient_type='all_faculty')
                for f in faculty_all:
                    Notification.objects.create(
                        recipient=f, title=f'New Notice: {title}',
                        message=body[:140], notification_type='general')
            self.stdout.write(f'✅ {len(notice_plan)} notices sent to faculty')

            # A few unread student notifications so the bell shows a badge.
            notif = []
            for stu in User.objects.filter(role='student'):
                notif.append(Notification(
                    recipient=stu, title='New resource uploaded',
                    message='Unit 1 lecture notes are now available for your subjects.',
                    notification_type='resource'))
                notif.append(Notification(
                    recipient=stu, title='Sessional 2 marks published',
                    message='Your Sessional 2 results have been published. Check the Marks page.',
                    notification_type='marks'))
            Notification.objects.bulk_create(notif, batch_size=500)
            self.stdout.write(f'✅ {len(notif)} student notifications')

        self.stdout.write(self.style.SUCCESS('''
🎉 Seeding complete! Credentials:

HOD:
  Username: hod_cs
  Password: HOD@1234

Faculty:
  prof_sharma / Faculty@1234
  prof_gupta  / Faculty@1234
  prof_verma  / Faculty@1234
  prof_singh  / Faculty@1234

Students (120 total):
  Format: s{sem}{section}{number}
  Example: s6a01 / Student@1234
  Example: s6b05 / Student@1234
        '''))