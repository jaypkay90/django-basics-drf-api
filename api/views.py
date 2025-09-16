from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from .serializers import EmployeeSerializer
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .paginations import CustomPagination

# Create your views here.
'''FUNCTION BASED VIEWS'''
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
    
    

'''CLASS BASED VIEWS'''
# Class Based Views akzeptieren keinen Decorator. Stattdessen wird innnerhalb der Klasse in Form von Methoden definiert, 
# was bei den jeweiligen HTTP-Methoden passieren soll
""" class Employees(APIView):
    def get(self, request):
        # Code komplett identisch zum Function Based View
        # Alle Employees aus DB ziehen -> Serialisierung -> JSON returnen
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Code komplett identisch zum Function Based View
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetailView(APIView):
    def get_object(self, pk):
        try:
            # Ziehe Employee mit entsprechender ID aus DB
            employee = Employee.objects.get(pk=pk)
            return employee
        except Employee.DoesNotExist:
            # Employee existiert nicht -> HTTP 404 Not Found
            raise Http404
    
    def get(self, request, pk):
        # self.get_object(pk) wird aufgerufen -> Employee mit entsprechender ID wird aus DB gezogen
        # Existiert der Mitarbeiter nicht, wird in get_object eine Http404-Exception geworfen, sodass der Code nach dieser Zeile abbricht
        employee = self.get_object(pk)
        
        # Serialisierung und Rückgabe der Daten im JSON-Format
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        # Mitarbeiter mit entsprechender ID aus DB ziehen, existiert er nicht, wird in get_object() eine Exception geworfen und der Code bricht ab
        employee = self.get_object(pk)

        # Code von hier an identisch mit function based view
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # Code komplett identisch mit Function Based View
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """


'''MIXIN BASED VIEWS/GENERIC CLASS BASED VIEWS'''
# Die CRUD-Operationen lassen sich mit Hilfe von Mixins viel einfacher implementieren
# Mixin: Eine Klasse, die ergänzende Funktionalitäten zur Superklasse bereitstellt, auf die über Vererbung zugegriffen werden kann
# Ein Mixin ist selbst keine Basisklasse. Es ist davon abhängig, dass alle Methoden und Attribute, die im Mixin verwendet werden, in 
# der eigentlichen Superklasse vorhanden sind.
# Gernerics: Generische Klassen sind allgemeine Klassen, die mit unterschiedlichen Datentypen arbeiten können.
# Mixins in Django Rest Framework: DRF bietet für alle CRUD-Operationen Mixins an. Man erspart sich dadurch eine Menge Zeilen Code, 
# weil in den Mixins bereits alles erledigt wird.
# GenericAPIView: GenericAPIView erbt von APIView und erweitert diese Klasse um nützliche Methoden, um z.B. automatisch mit serializern zu arbeiten, 
# mit der DB zu interagieren und HTTP-Requests sowie Responses zu verarbeiten
# MRO: Method Resolution Order - Python erlaubt Mehrfachvererbung. Die Reihenfolge, in der die Superklassen in der Parameterliste aufgeführt werden 
# bestimmt die Reihenfolge der Methodensuche. Die eigentliche Superklasse sollte immer ganz rechts stehen, Mixins links. Das ist deshalb so, weil 
# bei Methodenüberschreibung die Klassen in der Parameterliste von links nach rechts durchsucht werden.
'''
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # Diese beiden Attribute aus GenericAPIView sind notwendig, damit das Ganze funktioniert
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Get-Request -> Aufruf von list() aus ListModelMixin -> Alle Employees aus DB ziehen -> Serialisierung -> JSON returnen
    def get(self, request):
        return self.list(request)
    
    # Post-Request -> Aufruf von create() aus CreateModelMixin -> Deserialisierung -> In DB eifügune und JSON-Response returnen
    def post(self, request):
        return self.create(request)


class EmployeeDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView): 
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Get-Request -> Aufruf von retrieve() aus RetrieveModelMixin -> Einzelnen Employee anhand des PK aus DB ziehen -> Serialisierung -> JSON returnen
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    # Put-Request -> Aufruf von update() aus UpdateModelMixin -> Deserialisierung -> DB-Eintrag updaten und JSON-Response returnen
    def put(self, request, pk):
        return self.update(request, pk)
    
    # Delete-Request -> Aufruf von destroy() aus DestroyModelMixin -> Einzelnen Employee anhand des PK aus DB löschen
    def delete(self, request, pk):
        return self.destroy(request, pk)
'''

'''GENERIC CLASS BASED VIEWS'''
# DRF liefert folgende Generic Class Based Views: ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# So sieht ListCreateAPIView intern aus: class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView)
# Letztendlich sind die Generic Class Based Views von Django einfach eine Kombination aus Mixins und GenericAPIView, wie wir es weiter oben implementiert haben
# Die Mixins liefern die CRUD-Operationen, die GenericAPIView erweitert API-View um hilfreiche Methoden, um z.B. automatisch mit Models und Serializers zu arbeiten
# Dadurch kann man den Code deutlich kürzen
'''
class Employees(generics.ListCreateAPIView): # oder: class Employees(generics.ListAPIView, generics.CreateAPIView)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView): # oder: class EmployeeDetailView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
'''

'''VIEWSET'''
# Viewsets: Bislang haben wir für die Arbeit mit einzelnen Employees und der gesamten Employee-Liste zwei verschiedene Views implementiert
# Mit Viewsets kann man mehrere Views zu einer einzigen View zusammenfassen. Das URL-Handling übernimmt hierbei der DefaultRouter von DRF (implementiert in urls.py)
# Die Basisklass ViewSet braucht für jede CRUD-Operation eine Methode, die implementiert werden muss -> list, create, retrieve, update, delete
# Das ModelViewSet hingegen macht alle CRUD-Operationen vollständig automatisch -> es braucht dafür lediglich ein queryset und die zugehörige Serializer-Klasse
# Alternativ kann man mit der Klasse GenericViewSet, das auf GenericAPIView basiert (siehe oben) in Kombination mit Mixins nur bestimmte CRUD-Operaionen implementieren
'''
class EmployeeViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Custom Pagination implementieren -> festglegt in .paginations.py
    pagination_class = CustomPagination


'''BLOG VIEWS'''
# Wir wollen für Blog und Kommentare nur zwei CRUD-Operationen realisieren: Create (neuen Blog oder Kommentar erstellen) und List (alle Blogs und Kommentare anzeigen)
class BlogView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'