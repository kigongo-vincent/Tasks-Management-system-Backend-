from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        
class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"