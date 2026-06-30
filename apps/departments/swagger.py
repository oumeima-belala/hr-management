from core.swagger import *

from .serializers import *

def department_list_docs():

    return list_docs(

        tag="Departments",

        serializer=DepartmentListSerializer,

        description="Retrieve all departments."
    )