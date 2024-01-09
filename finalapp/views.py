import uuid
import random
from django import forms
from finalapp import models
from finalapp.school import *
from datetime import datetime
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from finalapp.finalapp import fee_id, get_fee, total_
from finalapp.models import *
from finalapp.forms import *
from django.http import HttpResponse,HttpResponseRedirect,BadHeaderError
from django.contrib import messages
from django.contrib.auth.models import User,auth
from email.message import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from finalapp.school import get_student_by_id
from django.utils import timezone

# Create your views here.
def base(request):
    return render(request,'base.html')
def home(request):
    return render(request,'home.html')
def contactus(request):
    return render(request,'contactus.html')
def aboutus(request):
    return render(request,'aboutus.html')

@login_required
def student_page(request):
    s = Student.objects.all()
    return render(request,'student_page.html',{'s':s})
def teacher_page(request):
    t = Teacher.objects.all()
    return render(request,'teacher_page.html',{'t':t})
def studentdata(request):
    data=Userdata1.objects.all()
    return render(request,"studentdata.html",{'d':data})
def teacherdata(request):
    data=Userdata.objects.all()
    return render(request,"teacherdata.html",{'k':data})
def add_student_details(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        Firstname=request.POST.get('Firstname')
        sd=Student.objects.get(id=Firstname)
        sd.delete()
    c=get_student(request)
    context={'c':c}
    return render(request,'add_student_details.html',context)

def student_details(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        Firstname=request.POST.get('Firstname')
        sd=Student.objects.get(id=Firstname)
        sd.delete()
    c=get_student(request)
    context={'c':c}
    return render(request,'student_detail.html',context)

def add_student(request):
    if request.method == 'POST':
        form = StudentData(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = StudentData()

    return render(request, 'add_student.html', {'form': form})
    
def add_teacher_details(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        Firstname=request.POST.get('Firstname')
        td=Teacher.objects.get(id=Firstname)
        td.delete()
    d=get_teacher(request)
    context={'d':d}
    return render(request,'add_teacher_details.html',context)

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')
    else:
        form = TeacherForm()

    return render(request, 'add_teacher.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('finalapp:student_page')  # Change the redirection URL to your desired home page
        else:
            messages.info(request, 'Invalid user credentials')
            return redirect('finalapp:student_login')
    else:
        return render(request, 'student_login.html')

def student_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        password2 = request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('finalapp:student_register')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('finalapp:student_login')
    else:
        return render(request, 'student_register.html')

def teacher_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('finalapp:teacher_page')
        else:
            messages.info(request,'Invalid user credentials')
            return redirect('finalapp:teacher_login')
    else:
        return render(request,'teacher_login.html')

def teacher_logout(request):
    auth.logout(request)
    return redirect('finalapp:home') 

def send_otp(email,otp):
    subject="OTP Verification"
    message=f'Your OTP for registration is: {otp}'
    send_mail(subject,message,None,[email])

def teacher_register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass1']
        password2=request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already taken")
            return redirect('finalapp:teacher_register')
        otp_number=random.randint(1000,9999)
        otp=str(otp_number)
        send_otp(email,otp)
        request.session['username']=username
        request.session['email']=email
        request.session['password']=password
        request.session['password2']=password2
        request.session['otp']=otp 
        return HttpResponseRedirect(reverse('finalapp:otp',args=[otp,username,password,email]))
    else:
        return render(request,'teacher_register.html')

def otp(request,otp,username,password,email):
    if request.method=="POST":
        uotp=request.POST['uotp']
        otp_from_session=request.session.get('otp')

        if uotp==otp_from_session:
            username=request.session.get('username')
            email=request.session.get('email')
            password=request.session.get('password')
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            return redirect('finalapp:teacher_login')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('finalapp:otp',otp=otp,username=username,password=password,email=email)
    return render(request,'otp.html',{'otp':otp ,'username':username,'password':password,'email':email})
        
def send_email(request):
    subject = request.POST.get("subject", "Confirmation mail")
    message = request.POST.get("message", "otp is 25312")
    from_email = request.POST.get("from_email", "tksiva05@gmail.com")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["tksiva05@gmail.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("Mail sent successfully.")
    else:
        return HttpResponse("Make sure all fields are entered and valid.")

def class_list(request):
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})

def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = ClassForm()

    return render(request, 'add_class.html', {'form': form})

#Admission Form
def student_admission_request(request):
    if request.method == 'POST':
        form = StudentAdmissionRequestForm(request.POST)
        if form.is_valid():
            student_form = form.save()
            admission_request = StudentAdmission.objects.create(student_form=student_form)
            return redirect('finalapp:student_admission_request_success')
        print('---------------------',form.errors)
    else:
        form = StudentAdmissionRequestForm()
    return render(request, 'student_admission_request.html', {'form': form})

def student_admission_request_success(request):
    return render(request, 'student_admission_request_success.html')

def view_student_admission_requests(request):
    admission_requests = StudentAdmission.objects.all()
    return render(request, 'view_student_admission_requests.html', {'admission_requests': admission_requests})

#Admin login

def schooladmin_login(request):
    if request.method == 'POST':
        entered_username = request.POST['username']
        entered_password = request.POST['password']

        # Check if the entered username and password match the fixed values
        fixed_username = 'admin'
        fixed_password = 'admin'

        if entered_username == fixed_username and entered_password == fixed_password:
            # Redirect to the desired page upon successful login
            return redirect('finalapp:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('finalapp:schooladmin_login')
   
    return render(request, 'admin_login.html')

def schooladmin_logout(request):
    return redirect('finalapp:home')

def dashboard(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    class_count = Class.objects.count()
    subject_count=Subject.objects.count()
    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'class_count': class_count,
        'subject_count': subject_count,
    }
    return render(request, 'dashboard.html', context)

#Subject
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'form': form})

#Questions
def upload_question_paper(request):
    if request.method == 'POST':
        form = QuestionPaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            question_paper = form.save(commit=False)
            question_paper.uploaded_by = request.user
            question_paper.save()
            return redirect('finalapp:success')
    else:
        form = QuestionPaperUploadForm()
    return render(request, 'upload_question_paper.html', {'form': form})

def view_question_papers(request):
    question_papers = QuestionPaper.objects.all()
    return render(request, 'view_question_papers.html', {'question_papers': question_papers})

#Result
def upload_results(request):
    if request.method == 'POST':
        form = ResultForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('finalapp:success')  # Redirect to a success page
    else:
        form = ResultForm()
    return render(request, 'upload_results.html', {'form': form})

def view_results(request):
    results = Result.objects.all()
    return render(request, 'view_results.html', {'results': results})

#Leave
def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.save()
            return redirect('finalapp:leave_request_success')  # Redirect to a success page
        else:
            print(form.errors) 
    else:
        form = LeaveRequestForm()    

    return render(request, 'leave_request.html', {'form': form})

def leave_request_success(request):
    return render(request, 'leave_request_success.html')

def view_leave_requests(request):
    leave_requests = TeacherLeave.objects.all()
    return render(request, 'view_leave_requests.html', {'leave_requests': leave_requests})

def approve_leave(request, leave_id):
    leave_request = TeacherLeave.objects.get(pk=leave_id)
    leave_request.is_approved = True
    leave_request.save()
    return redirect('finalapp:view_leave_requests')

def reject_leave(request, leave_id):
    leave_request = TeacherLeave.objects.get(pk=leave_id)
    leave_request.is_approved = False
    leave_request.is_rejected = True  # Update is_rejected field to True
    leave_request.save()
    return redirect('finalapp:view_leave_requests')


def view_leave_requests_table(request):
    leave_requests = TeacherLeave.objects.all()
    return render(request, 'view_leave_requests_table.html', {'leave_requests': leave_requests})

#Fee
def update_fee(request):
    if request.method == 'POST':
        form = FeeUpdateForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.student = request.user  # Assign the User instance to fee.student
            fee.updated_by = request.user
            fee.save()
            return redirect('finalapp:view_feesadmin')
    else:
        form = FeeUpdateForm()
    return render(request, 'update_fee.html', {'form': form})

def view_feesadmin(request):
    fees = Fee.objects.all()
    return render(request, 'view_feesadmin.html', {'fees': fees})  

#Notice
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice_list.html', {'notices': notices})

def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            admin_user, created = User.objects.get_or_create(username='admin')
            if created:
                admin_user.set_password('admin')  # Set the password
                admin_user.save()

            notice.author = admin_user
            notice.save()
            return redirect('finalapp:success')
    else:
        form = NoticeForm()
    return render(request, 'add_notice.html', {'form': form})

#Contact Us
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'success.html')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})

#Success 
def success(request):
    return render(request, 'success.html')

#Attendance
def attendance_form(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            # You can redirect to a success page or any other page after saving the form
            return redirect('finalapp:success')
    else:
        form = AttendanceForm()

    return render(request, 'attendance_form.html', {'form': form})

def view_attendance(request):
    o=Attendance.objects.all()
    context={'o':o}
    return render(request,'view_attendance.html',context)