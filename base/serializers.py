from rest_framework.serializers import ModelSerializer, CharField, EmailField
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CompanySerializer(ModelSerializer):
    admin_email = EmailField(source = "admin.email", read_only = True)
    class Meta:
        model = Company
        fields = "__all__"

class TaskSerializer(ModelSerializer):
    project_name = CharField(source = "project.name", read_only = True)
    class Meta:
        model = Task
        fields = "__all__"
        
class DepartmentSerializer(ModelSerializer):
    admin_email = EmailField(source = "admin.email", read_only = True)
    class Meta:
        model = Department
        fields = "__all__"

class ProjectSerializer(ModelSerializer):
    
    class Meta:
        model = Project
        fields = "__all__"