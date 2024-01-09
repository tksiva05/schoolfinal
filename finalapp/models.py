from django import forms
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=120)
    Lastname = models.CharField(max_length=120)
    Email = models.EmailField(max_length=50, unique=True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Password = models.CharField(max_length=20)
    Address = models.TextField()
    Subject = models.CharField(max_length=20)

    def __str__(self):
        return self.Firstname

    @staticmethod
    def total_teachers():
        return Teacher.objects.count() 

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Class_CHOICES = [
        ('class1','class1'),
        ('class2','class2'),
        ( 'class3','class3'),
        ( 'class4' ,'class4'),
        ( 'class5','class5'),
        ( 'class6','class6'),
        ( 'class7','class7'),
        ( 'class8','class8'),
        ( 'class9','class9'),
        ( 'class10', 'class10'),    
    ]
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    Firstname = models.CharField(max_length = 120)
    Lastname = models.CharField(max_length = 120)
    Email = models.EmailField(max_length = 50, unique = True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Password = models.CharField(max_length = 20)
    Profile = models.ImageField(upload_to = '')
    Co = models.CharField(max_length=10, choices=Class_CHOICES)
    Session = models.DateTimeField(auto_now_add = True)
    @classmethod
    def total_students(cls):
        return cls.objects.count()
    # Other fields for your Student model

    def total_present_days(self):
        return self.attendance_set.filter(is_present=True).count()
    def __str__(self):
        return f"{self.Firstname} - {self.Co}"
 
class Userdata(models.Model):
    Username=models.CharField(max_length=20)
    Email=models.EmailField(max_length=30)
    Password=models.CharField(max_length=10)
    def __str__(self):
        return self.Username

class Userdata1(models.Model):
    Username=models.CharField(max_length=20)
    Email=models.EmailField(max_length=30)
    Password=models.CharField(max_length=10)
    def __str__(self):
        return self.Username

class Class(models.Model):
    name = models.CharField(max_length=120)
    academic = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    # credit = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TeacherLeave(models.Model):
    teacher = models.ForeignKey('finalapp.Teacher', on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher} - {self.start_date} to {self.end_date}"
def __str__(self):
    status = "Pending"
    if self.is_approved:
        status = "Approved"
    elif self.is_rejected:
        status = "Rejected"
    return f"{self.teacher} - {self.start_date} to {self.end_date} ({status})"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def _str_(self):
        return self.name

class StudentForm(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    GRADE_CHOICES = [
        ('1', 'class1'),
        ('2', 'class2'),
        ('3', 'class3'),
        ('4', 'class4'),
        ('5', 'class5'),
        ('6', 'class6'),
        ('7', 'class7'),
        ('8', 'class8'),
        ('9', 'class9'),
        ('10', 'class10'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    enter_dob = models.DateField() 
    parent_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15)
    enter_email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    address = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StudentAdmission(models.Model):
    student_form = models.ForeignKey(StudentForm, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.student_form.first_name} {self.student_form.last_name} Admission"
 
class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class QuestionPaper(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='question_papers/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Fee(models.Model):
    fee_id=models.CharField(max_length=20)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_fees')
    updated_at = models.DateTimeField(auto_now_add=True)
    def total(self):
        return self.amount

class Result(models.Model):
    class_name = models.CharField(max_length=100)
    result_file = models.FileField(upload_to='result_files/')

class Attendance(models.Model):
    PRESENT = 'Present'
    ABSENT = 'Absent'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present_status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.Firstname} - {self.date} - {self.present_status}"

    