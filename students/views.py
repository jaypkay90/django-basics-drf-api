from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def students(request):
    students = [
        {'id': 1, 'name': 'John Doe', 'age': 25},
        {'id': 2, 'name': 'Jane Bee', 'age': 27}
    ]
    return HttpResponse(students)
    #return render(request, 'students.html')