
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import uploaded_data, MyUser
from .forms import FileUploadForm
from django.contrib import messages
import pandas as pd
import sqlite3
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required as django_login_required
from django.contrib.auth.hashers import make_password, check_password
import logging
from .decorators import custom_login_required  # Import the custom decorator


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        user = MyUser(username=username, password=make_password(password))
        user.save()
        login(request, user)
        return redirect('upload_file')
    return render(request, 'fileupload/signup.html')

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_file')
        else:
            messages.error(request, 'Invalid username or password')
            logger.error(f'Login failed for username: {username}')
    return render(request, 'fileupload/signin.html')

def home_view(request):
    return render(request, 'fileupload/index.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@custom_login_required  # Apply the custom decorator
def get_batch_names(request):
    report_name = request.GET.get('report_name')
    batch_names = uploaded_data.objects.filter(
        report_name=report_name, batch_name__isnull=False).values_list('batch_name', flat=True).distinct()
    return JsonResponse({'batch_names': list(batch_names)})

@custom_login_required  # Apply the custom decorator
def get_subject_names(request):
    batch_name = request.GET.get('batch_name')
    subject_names = uploaded_data.objects.filter(
        batch_name=batch_name, subject_name__isnull=False).values_list('subject_name', 'subject_code').distinct()
    return JsonResponse({'subject_names': list(subject_names)})

def load_data(df, sqlite_file_path, table_name, is_ug, report_name):
    column_mapping = {
        'Exam Code': 'exam_code',
        'Student Batch Name': 'student_batch_name',
        'Batch Name': 'batch_name',
        'Class Name': 'class_name',
        'Student Name': 'student_name',
        'RegNo': 'reg_no',
        'Roll No': 'roll_no',
        'Exam Type': 'exam_type',
        'Subject Type': 'subject_type',
        'Subject Code': 'subject_code',
        'Subject Name': 'subject_name',
        'Semester': 'semester',
        'Obt Marks': 'obt_marks',
        'Max Marks': 'max_marks',
        'Obt Grade': 'obt_grade',
        'Is Backlog': 'is_backlog',
        'Is Pass': 'is_pass',
        'Backlog Attempt Number': 'backlog_attempt_number',
        'Credit Point Earned': 'credit_point_earned',
        'Credit Point Offered': 'credit_point_offered',
        'RV Marks': 'rv_marks',
        'RV Updated': 'rv_updated',
    }

    df.rename(columns=column_mapping, inplace=True)
    df['course_category'] = 'UG' if is_ug else 'PG'
    df['report_name'] = report_name

    df['exam_type'] = df['exam_type'].replace({
        'Formative Assessment (FA)': 'FA',
        'Summative Assessment (SA)': 'SA'
    })

    df = df.sort_values(by='roll_no')
    df['obt_marks'] = df.apply(lambda x: '' if (x['exam_type'] in ['Aggregate', 'SA'] and x['obt_marks'] == 0) else x['obt_marks'], axis=1)

    conn = sqlite3.connect(sqlite_file_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
   

@custom_login_required  # Apply the custom decorator
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        course_category = request.POST['course_category']
        report_name = request.POST['report_name']

        if form.is_valid():
            uploaded_file = request.FILES['input_excel']
            df = pd.read_excel(uploaded_file)

            # Ensure course_category is either 'UG' or 'PG'
            if course_category.upper() in dict(uploaded_data.COURSE_CATEGORIES):
                is_ug = (course_category == uploaded_data.UG)
            else:
                is_ug = False

            load_data(df, "db.sqlite3", "fileupload_uploaded_data", is_ug, report_name)

            # Add a success message
            messages.success(request, 'File uploaded and data saved successfully!')
        else:
            messages.error(request, 'Form is not valid. Please check the input.')

    else:
        form = FileUploadForm()
    
    return render(request, 'fileupload/upload.html', {'form': form})

@custom_login_required  # Apply the custom decorator
def generate_report(request):
    excel_data = uploaded_data.objects.all()

    reports = uploaded_data.objects.values_list('report_name', flat=True).distinct()
    context = {
        'excel_data': excel_data,
        'reports': reports
    }

    return render(request, 'fileupload/generate_report.html', context)

@custom_login_required  # Apply the custom decorator
def filtered_report(request):
    report_name = request.POST['report_name']
    batch_name = request.POST['batch_name']
    subject_code = request.POST['subject']

    filtered_data = uploaded_data.objects.filter(report_name=report_name, batch_name=batch_name, subject_code=subject_code).values()

    fd_df = pd.DataFrame.from_records(filtered_data)

    subject_name = fd_df['subject_name'].iloc[0] if not fd_df.empty else None

    rows = []
    if not fd_df.empty:
        for roll_no in fd_df['roll_no'].unique():
            student_data = fd_df[fd_df['roll_no'] == roll_no]
            for subject in student_data['subject_code'].unique():
                subject_data = student_data[student_data['subject_code'] == subject]
                if not subject_data.empty:
                    row = {
                        'roll_no': roll_no,
                        'student_name': subject_data.iloc[0]['student_name'],
                        'batch_name': subject_data.iloc[0]['batch_name'],
                        'subject_name': subject_data.iloc[0]['subject_name'],
                        'fa': subject_data[subject_data['exam_type'] == 'FA']['obt_marks'].values[0] if not subject_data[subject_data['exam_type'] == 'FA'].empty else '',
                        'sa': subject_data[subject_data['exam_type'] == 'SA']['obt_marks'].values[0] if not subject_data[subject_data['exam_type'] == 'SA'].empty else '',
                        'aggregate': subject_data[subject_data['exam_type'] == 'Aggregate']['obt_marks'].values[0] if not subject_data[subject_data['exam_type'] == 'Aggregate'].empty else '',
                        'obt_grade': subject_data[subject_data['exam_type'] == 'Aggregate']['obt_grade'].values[0]
                    }
                    rows.append(row)
    
    fd_df['obt_marks'] = pd.to_numeric(fd_df['obt_marks'], errors='coerce')

    # Calculate summary values
    max_sa = fd_df[fd_df['exam_type'] == 'SA']['obt_marks'].max() if not fd_df[fd_df['exam_type'] == 'SA']['obt_marks'].dropna().empty else None
    min_sa = fd_df[fd_df['exam_type'] == 'SA']['obt_marks'].min() if not fd_df[fd_df['exam_type'] == 'SA']['obt_marks'].dropna().empty else None
    max_agg = fd_df[fd_df['exam_type'] == 'Aggregate']['obt_marks'].max() if not fd_df[fd_df['exam_type'] == 'Aggregate']['obt_marks'].dropna().empty else None
    min_agg = fd_df[fd_df['exam_type'] == 'Aggregate']['obt_marks'].min() if not fd_df[fd_df['exam_type'] == 'Aggregate']['obt_marks'].dropna().empty else None
    count_f_grades = len(fd_df[fd_df['obt_grade'] == 'F']) if 'obt_grade' in fd_df.columns else 0

    context = {
        'subject_name' : subject_name,
        'report_data': rows,
        'max_sa': max_sa,
        'min_sa': min_sa,
        'max_agg': max_agg,
        'min_agg': min_agg,
        'count_f_grades': count_f_grades
    }
   
    return render(request, 'fileupload/filtered_data.html', context)
