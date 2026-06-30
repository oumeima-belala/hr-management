from core.swagger import *

from .serializers import *

def employee_list_docs():

    return list_docs(

        tag="Employees",

        serializer=EmployeeListSerializer,

        description="Retrieve all employees."
    )