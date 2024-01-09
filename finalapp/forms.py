from django import forms
from finalapp.models  import Attendance,TeacherLeave, Subject,Student,Class, Notice,Fee,QuestionPaper, Result, Subject, Userdata,Userdata1,TeacherLeave,Contact,StudentForm,Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
class StudentData(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class Userform(forms.ModelForm):
    class Meta:
        model=Userdata
        fields=['Username','Email','Password']

class Userform1(forms.ModelForm):
    class Meta:
        model=Userdata1
        fields=['Username','Email','Password']

class LeaveRequestForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}
        ),
        input_formats=['%Y-%m-%d', '%d-%m-%Y']
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}
        ),
        input_formats=['%Y-%m-%d', '%d-%m-%Y']
    )

    class Meta:
        model = TeacherLeave
        fields = ['teacher', 'reason', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date should be after the start date")

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class StudentAdmissionRequestForm(forms.ModelForm):
    class Meta:
        model = StudentForm
        fields = '__all__'
        widgets = {
            'enter_dob': forms.DateInput(attrs={'type': 'date'}),
        }
    
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content' ]

class QuestionPaperUploadForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['title', 'file']

class FeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['class_name', 'amount']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        
class AskDateForm(forms.Form):
    date=forms.DateField()
    
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['class_name', 'result_file']

class DateSelectionForm(forms.Form):
    attendance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'present_status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }