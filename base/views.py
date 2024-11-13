from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod

    def get_token(cls, user):

        token = super().get_token(user)

        # Add custom claims to the token payload

        token['role'] = user.role

        token['username'] = user.username

        token['email'] = user.email

        token['contact'] = user.contact

        try:
            token['company'] = user.department.company.id
        except: 
            token['company'] = None

        return token
    

# creating a custom serializer for information encoded in the tokens 

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST', 'GET'])
def companies(request):
    try:
        if request.method == "POST":
            serialized = CompanySerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                serialized.data["admin_email"] = UserSerializer(User.objects.get(id = serialized.data["admin"])).data["email"]
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        companies = Company.objects.all()
        serialized = CompanySerializer(companies, many = True)
        for company in serialized.data:
            company["admin_email"] = UserSerializer(User.objects.get(id = company["admin"])).data["email"]
        return Response(serialized.data)  
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

@api_view(['PATCH', 'DELETE', 'GET'])
def company(request, pk):

    try:
        company =Company.objects.get(id = pk)
        company_head = User.objects.get(id = company.admin.id)

        if request.method == "PATCH":
            print(request.data)
            
            serialized = CompanySerializer(company, data = request.data, partial = True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            try:
                company_head = User.objects.get(id = company.admin.id)
                company_head.delete()
            except:
                pass      
            company.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        elif request.method == "GET":
            serialized = CompanySerializer(company)
            return Response(serialized.data)
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT) 
       
@api_view(['PATCH', 'DELETE', 'GET'])
def department(request, pk):

    try:
        department =Department.objects.get(id = pk)

        if request.method == "PATCH":
            serialized = DepartmentSerializer(department, data = request.data, partial = True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":    
            try:
                department_head = User.objects.get(id = department.admin.id)
                department_head.delete()
            except:
                pass    
            department.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        elif request.method == "GET":
            serialized = DepartmentSerializer(department)
            return Response(serialized.data)
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)  
      
@api_view(['PATCH', 'DELETE', 'GET'])
def task(request, pk):

    try:
        task =Task.objects.get(id = pk)

        if request.method == "PATCH":
            serialized = TaskSerializer(task, data = request.data, partial = True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":    
            task.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        elif request.method == "GET":
            serialized = TaskSerializer(task)
            return Response(serialized.data)
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)    
    

@api_view(['GET', 'POST'])
def company_admins(request):
    try:
        if request.method == "POST":
            request.data["password"] = make_password(request.data["password"])
            request.data["role"] = "company_admin"
            serialized = UserSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        company_admins = User.objects.filter(role = "company_admin")
        serialized = UserSerializer(company_admins, many = True)
        return Response(serialized.data)    
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)
    

@api_view(['GET', 'POST'])
def departments(request, pk):
    if request.method == "POST":
        request.data["company"] = pk
        serialized = DepartmentSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            serialized.data["admin_email"] = UserSerializer(User.objects.get(id = serialized.data["admin"])).data["email"]
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
    departments = Department.objects.filter(company = pk) 
    serialized = DepartmentSerializer(departments, many = True)
    for department in serialized.data:
            department["admin_email"] = UserSerializer(User.objects.get(id = department["admin"])).data["email"]
    return Response(serialized.data)   

    
@api_view(['GET', 'POST'])
def department_admins(request, pk):
    try:
        if request.method == "POST":
            request.data["password"] = make_password(request.data["password"])
            request.data["role"] = "department_admin"
            request.data["company"] = pk
            serialized = UserSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        department_admins = User.objects.filter(role = "department_admin", company = pk)
        serialized = UserSerializer(department_admins, many = True)
        return Response(serialized.data)    
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)
    

@api_view(["GET", "POST"])
def employees(request, pk):
    try:
        if request.method == "POST":
            request.data["role"] = "employee"
            request.data["password"] = make_password(request.data["password"])
            request.data["department"] = pk
            serialized = UserSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        employees = User.objects.filter(role = "employee", department = pk)
        serialized = UserSerializer(employees, many =True)
        return Response(serialized.data)    

    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)


@api_view(["GET", "POST"])
def tasks(request, pk):
    try:
        if request.method == "POST":
            request.data["employee"] = pk
            serialized = TaskSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(employee = pk)
        serialized = TaskSerializer(tasks, many =True)
        return Response(serialized.data)    

    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)
    

@api_view(['GET'])
def get_company(request, pk):
    try:
        company = Company.objects.get(admin = pk)
        serialized = CompanySerializer(company)
        return Response(serialized.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_department(request, pk):
    try:
        department = Department.objects.get(admin = pk)
        serialized = DepartmentSerializer(department)
        return Response(serialized.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)    

@api_view(['PATCH'])    
def update_user(request, pk):
    try:
        user = User.objects.get(id = pk)
        try:
            if request.data["password"]:
                request.data["password"] = make_password(request.data["password"])
        except:
            pass        
        serialized = UserSerializer(user, data = request.data, partial= True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status = status.HTTP_418_IM_A_TEAPOT)    


@api_view(['DELETE'])
def user(request, pk):
    try:
        user = User.objects.get(id = pk)
        user.delete()
        return Response(status = status.HTTP_202_ACCEPTED)
    except:    
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def projects(request, pk):

    if request.method == "POST":
        request.data["company"] =pk
        serialized = ProjectSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status = status.HTTP_201_CREATED)

    projects = Project.objects.filter(company = pk)
    serialized = ProjectSerializer(projects, many = True)
    return Response(serialized.data)


@api_view(['PATCH', 'DELETE'])
def project(request, pk):
    try:
        project = Project.objects.get(id = pk)
    except:
        project = None

    if project is None:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        project.delete()
        return Response(status = status.HTTP_202_ACCEPTED)

    if request.method == "PATCH":
        serialized = ProjectSerializer(project, data = request.data, partial = True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status = status.HTTP_202_ACCEPTED)




''''
apis needed

auth
-signin

super admin
-post comapny
-post company head
-update company
-delete company

company head
-post department
-post department head
-get departments
-get employees in a department
-get tasks for employees in a department

department head
-post employee
-update employee
-get employees in a department
-get tasks for employees in a department

employee
-post task
-view tasks
-update employee
'''