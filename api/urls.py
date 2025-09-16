from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Viewset Routing -> mithilfe des DefaultRouter() Objekts werden die URLs für den Aufruf einzelner employees und der employeeListe automatisch erzeugt, sodass man nur noch
# eine einzige View implementieren muss
router = DefaultRouter()
router.register('employees', views.EmployeeViewset, basename='employees')

urlpatterns = [
    # Function Based Views
    path('students/', views.studentsView, name='students_View'),
    path('students/<int:pk>/', views.studentDetailView, name='student_Detail_View'),

    # Class Based View
    # path('employees/', views.Employees.as_view(), name='employees_View'),
    # path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_Detail_View'),

    # Viewset Routing
    path('', include(router.urls)),

    # Blogs
    path('blogs/', views.BlogView.as_view(), name='blogs_View'),
    path('comments/', views.CommentsView.as_view(), name='comments_View'),

    # Blog Detail
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog_Detail_View'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_Detail_View'),
]