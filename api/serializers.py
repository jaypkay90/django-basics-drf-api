from rest_framework import serializers
from students.models import Student

'''Serialization: Objekte aus der Datenbank, also hier die Students, werden in ein Format umgewandelt, 
    das an das Frontend geschickt werden kann, meist JSON. Serializer sind sozusagen Übersetzer.
    Desireralization: Das Frontend schickt Daten im JSON-Format, die hier von einem Desirializer in Python-Objekte umgewandelt werden, 
    damit sie weiterverarbeitet werden können. 
    Manual Serialization: Der Code, der die Objekte in JSON umwandelt und ans Frontend weitergibt, wird selbst geschrieben
    Django Serializers: Django bietet Serializer an, die komplexe Datentypen in JSON oder XML umwandeln können. Am gängisten ist der Model-Serializer, 
    der Model-Objekte/Datenbankfelder in JSON oder XML umwandelt'''

# ein DRF Serializer kann auch desireralisieren
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        # Model, das serialisiert werden soll -> Student
        model = Student

        # Felder, die serialisiert bzw. im JSON erscheinen sollen.
        fields = '__all__'