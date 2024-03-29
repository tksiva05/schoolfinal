from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from finalapp.views import view_attendance, attendance_form, student_details, schooladmin_logout, schooladmin_login, teacher_logout, view_feesadmin, student_admission_request, student_admission_request_success, view_student_admission_requests, view_leave_requests_table, leave_request, leave_request_success, view_leave_requests, approve_leave, reject_leave, student_register, student_login, base, add_notice, add_class, add_subject, add_student, add_teacher, dashboard, add_teacher_details, class_list, subject_list, update_fee, upload_results, home, aboutus, contactus, notice_list, success, otp, teacher_login, add_student_details, teacher_register, studentdata, teacherdata, teacher_page, student_page, send_email, upload_question_paper, view_question_papers, view_results
app_name="finalapp"
urlpatterns =[
    path('attendance-form/', attendance_form, name='attendance_form'),
    path('student_login/',student_login,name='student_login'),
    path('student_register/',student_register,name='student_register'),
    path('base/',base,name="base"),
    path('',home,name='home'),
    path('c/',contactus,name='contactus'),
    path('a/',aboutus,name='aboutus'),
    path('success/', success, name='success'),
    path('tp/',teacher_page,name='teacher_page'),
    path('sp/',student_page,name='student_page'),
    path('tr/',teacher_register,name='teacher_register'),
    path('sd/',studentdata,name='studentdata'),
    path('td/',teacherdata,name='teacherdata'),
    path('sa/',add_student_details,name='add_student_details'),
    path('sdd/',student_details,name='student_details'),
    path('ta/',add_teacher_details,name='add_teacher_details'),
    path('mail/',send_email,name='send_email'),
    path('tl/',teacher_login,name='teacher_login'),
    path('otp/<str:otp>/<str:username>/<str:password>/<str:email>/',otp,name='otp'),
    #Teacher Leave
    path('leave_request/', leave_request, name='leave_request'),
    path('leave_request/success/', leave_request_success, name='leave_request_success'),
    path('view_leave_requests/', view_leave_requests, name='view_leave_requests'),
    path('approve_leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', reject_leave, name='reject_leave'),
    path('view_leave_requests_table/', view_leave_requests_table, name='view_leave_requests_table'),
    #Admission Form
    path('student_admission_request/', student_admission_request, name='student_admission_request'),
    path('student_admission_request_success/', student_admission_request_success, name='student_admission_request_success'),
    path('view_student_admission_requests/', view_student_admission_requests, name='view_student_admission_requests'),
    path('notice-list/', notice_list, name='notice_list'),
    path('add/', add_notice, name='add_notice'),
    path('upload-question-paper/', upload_question_paper, name='upload_question_paper'),
    path('view-question-papers/', view_question_papers, name='view_question_papers'),
    path('update-fee/',update_fee,name='update_fee'),
    path('view_feeadmin/',view_feesadmin,name='view_feesadmin'),
    path('classes/', class_list, name='class_list'),
    path('subjects/', subject_list, name='subject_list'),
    path('upload_results/', upload_results, name='upload_results'),
    path('view_results/', view_results, name='view_results'),
    path('dashboard/',dashboard,name='dashboard'),
    path('schooladmin_logout/', schooladmin_logout, name='schooladmin_logout'),
    path('add_teacher/', add_teacher, name='add_teacher'),
    path('add_student/', add_student, name='add_student'),
    path('add_class/', add_class, name='add_class'),
    path('add_subject/', add_subject, name='add_subject'),
    path('viewatt/',view_attendance,name="view_attendance"),
    path('teacher_logout/', teacher_logout, name='teacher_logout'),
    path('schooladmin_login/', schooladmin_login, name='schooladmin_login'), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)