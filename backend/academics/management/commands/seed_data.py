from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academics.models import Department, Subject, Section, Timetable
from users.models import StudentProfile, FacultyProfile
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