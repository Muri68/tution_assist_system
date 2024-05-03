from django.urls import path, include
from . import views


urlpatterns = [
    path('Dashboard/', views.UniversityDashboard, name='universityDashboard'),
    path('add-students/', views.universityAddStudent, name='universityAddStudents'),
    path('students/', views.universityAllStudent, name='universityStudents'),
    path('donations/', views.universityDonations, name='universityDonations'),
    path('students-campaign/', views.UniversityStudentsCampaign, name='universityStudentCampaign'),
    
    path("student/detail/<int:student_id>/", views.universityViewStudent, name='student_detail'),
    path('add-campaign/<int:student_id>/', views.UniversityAddStudentsCampaign, name='add-student-campaign'),
    path("student/edit/<int:student_id>", views.edit_student, name='edit_student'),
]