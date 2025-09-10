from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.studentsView, name='students_View'),
    path('student/<int:pk>/', views.studentDetailView, name='student_Detail_View'),
]