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
        # Get all students from DB
        students = Student.objects.all()

        # many=True -> mehrere Students werden übergeben -> ohne many=True erwartet der Serializer ein einzelnes Objekt
        # In dieser Zeile macht der StudentSerializer aus den Studenten aus der DB Python-Datenstrukturen (Dicts/Listen), die leicht in JSON umgewandelt werden können
        serializer = StudentSerializer(students, many=True)

        # serializer.data = Python-Datenstrukturen (Listen/Dictionaries)
        # Daten werden als JSON zurückgeben
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Deserialisierung -> JSON-Daten aus Frontend wird in ein internes Datenobjekt um, das dann überprüft/validiert werden kann
        serializer = StudentSerializer(data=request.data)

        # Validierung -> Entsprechen die Daten den Regeln, die im Student-Model festgelegt worden sind?
        if serializer.is_valid():
            # Neues Student-Objekt wird angelegt und danach die Daten in die DB geschrieben
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # User hat fehlerhafte Daten eingegeben
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def studentDetailView(request, pk):
    
    
