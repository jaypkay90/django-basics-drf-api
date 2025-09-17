import django_filters
from .models import Employee

# Erstellen eines Custom Filters
class EmployeeFilter(django_filters.FilterSet):
    # Filter Employees by designation -> Retrieve all employees whose designation is "Software Engineer"
    # in der URL steht der Name dieser Variable, also z.B. ?designation=Manager
    # field_name ist der Name des Feldes im Model, nach dem wir Filtern wollen
    # lookup_expr='iexact' -> wir akzeptieren Groß- und Kleinschreibung beim Filtern
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='iexact')
    
    # Filter Employees by name -> Retrieve all employees whose names CONTAIN the word "John"
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains')

    # Filter nach ID bzw. Primary Key
    # id = django_filters.RangeFilter(field_name='id')

    # Filter Employees by ID Range -> Retrieve all employees whose IDs are between "EMP002" and "EMP004"
    # Hinweis: Wir haben emp_id im Model als CharField gesetzt -> deshalb CharFilter
    # label: Beschriftung, die dem User für die Filteroption angezeigt wird
    # method: Funktion, die aufgerufen wird, um die Filterung durchzuführen
    id_min = django_filters.CharFilter(method='filter_by_id_range', label='From EMP ID')
    id_max = django_filters.CharFilter(method='filter_by_id_range', label='To EMP ID')

    class Meta:
        model = Employee

        # Felder aus dem Employee-Model, die gefiltert werden können
        # Wichtig: 'id_min' und 'id_max' sind nicht im Model definiert -> diese haben wir selbst definiert, um die EMP_ID's mit einem CustomFilter zu filtern
        fields = ['designation', 'emp_name', 'id_min', 'id_max']

    # Funktion zum Filtern der emp_id's nach ID Range -> emp_id ist ein CharField
    # name: Name des Filters, der gesetzt wird, value: Wert des Filters
    # GET /employees/?id_min=EMP002&id_max=EMP007 -> In so einem Fall wird die Funktion zweimal aufgerufen
    def filter_by_id_range(self, queryset, name, value):
        if name == 'id_min':
            # gte: greater than or equal -> Alle Werte die größer oder gleich dem vom User eingegebenen Wert sind werden herausgefiltert
            return queryset.filter(emp_id__gte=value)
        elif name == 'id_max':
            # lte: less than or equal -> Alle Werte die kleiner oder gleich dem vom User eingegebenen Wert sind werden herausgefiltert
            return queryset.filter(emp_id__lte=value)
        
        # Wenn name weder id_min noch id_max ist, wird das ursprüngl. queryset returned
        return queryset