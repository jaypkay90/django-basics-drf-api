from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
# API-View, die get und post akzeptiert
@api_view(['GET', 'POST'])
def studentsView(request):
    '''Serialization: Objekte aus der Datenbank, also hier die Students, werden in ein Format umgewandelt, 
    das an das Frontend geschickt werden kann, meist JSON. Serializer sind sozusagen Übersetzer.
    Desireralization: Das Frontend schickt Daten im JSON-Format, die hier von einem Desirializer in Python-Objekte umgewandelt werden, 
    damit sie weiterverarbeitet werden können. 
    Manual Serialization: Der Code, der die Objekte in JSON umwandelt und ans Frontend weitergibt, wird selbst geschrieben
    Django Serializers: Django bietet Serializer an, die komplexe Datentypen in JSON oder XML umwandeln können. Am gängisten ist der Model-Serializer, 
    der Model-Objekte/Datenbankfelder in JSON oder XML umwandelt'''

    # # Queryset aus allen Students aus der DB ziehen
    # students = Student.objects.all()

    # # Queryset in Liste aus Dictionaries umwandeln
    # student_list = list(students.values())
    # print(student_list)

    # # JSON Response erwartet ein Dictionary
    # # Damit die Liste angenommen wird, muss safe auf False gesetzt werden -> sonst gibt es einen Fehler
    # return JsonResponse(student_list, safe=False)

    if request.method == 'GET':
        # Get all students from DB -> Studenten werden als QuerySet aus DB gezogen
        students = Student.objects.all()

        # many=True -> mehrere Students werden übergeben -> ohne many=True erwartet der Serializer ein einzelnes Objekt
         # In dieser Zeile macht der StudentSerializer aus den Studenten-QuerySet ein Serializer-Objekt. Die Daten sind als Dictionary-Liste in serializer.data
        serializer = StudentSerializer(students, many=True)

        # serializer.data = Liste aus Dictionaries
        # Daten werden als JSON zurückgeben
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Deserialisierung -> JSON-Daten aus Frontend werden in einem Serializer-Objekt gespeichert
        serializer = StudentSerializer(data=request.data)

        # Validierung -> Entsprechen die Daten den Regeln, die im Student-Model festgelegt worden sind?
        if serializer.is_valid():
            # Neues Student-Objekt wird angelegt und danach die Daten in die DB geschrieben
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # User hat fehlerhafte Daten eingegeben
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk):
    try:
        # Student mit dem entsprechenden Primary Key als einzelnes Objekt aus der DB ziehen
        student = Student.objects.get(pk=pk)
    
    # Student mit PK nicht existent -> 404
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Student lesen/Infos aus DB ziehen
    if request.method == 'GET':
        # In dieser Zeile macht der StudentSerializer aus dem Student ein Serializer-Objekt. Die Daten sind als Dictionary in serializer.data
        serializer = StudentSerializer(student)

        # Rückgabe der Daten im JSON-Format
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Student updaten
    elif request.method == 'PUT':
        # Wir müssen dem serializer hier das Student-Objekt mitgeben! Tun wir das nicht, wird ein neues Student-Objekt erzeugt
        # In dieser Zeile macht der StudentSerializer aus dem spezifizierten Studenten, der über die API per PUT geupdated werden soll, ein Serializer-Objekt
        # Die Daten aus dem Frontend sind in request.data
        serializer = StudentSerializer(student, data=request.data)

        # Validierung -> Entsprechen die Daten den Regeln, die im Student-Model festgelegt worden sind?
        if serializer.is_valid():
            # Änderungen werden gespeichert und in DB geschrieben
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Student aus DB löschen
    elif request.method == 'DELETE':
        # Student aus DB löschen
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    


    
