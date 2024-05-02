from django.urls import path, include
from . import views


urlpatterns = [
    path('Dashboard/', views.UniversityDashboard, name='universityDashboard'),
    path('add-students/', views.universityAddStudent, name='universityAddStudents'),
    path('students/', views.universityAllStudent, name='universityStudents'),
    path('donations/', views.universityDonations, name='universityDonations'),
    path('students-campaign/', views.UniversityStudentsCampaign, name='universityStudentCampaign'),
    
    path("student/edit/<int:student_id>", views.edit_student, name='edit_student'),
]