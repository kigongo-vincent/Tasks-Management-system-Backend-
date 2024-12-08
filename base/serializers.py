from rest_framework.serializers import ModelSerializer, CharField, EmailField, IntegerField
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    company = IntegerField(source= "department.company.id", read_only = True)
    class Meta:
        model = User
        fields = "__all__"

class CompanySerializer(ModelSerializer):
    admin_email = EmailField(source = "admin.email", read_only = True)
    admin_first_name = EmailField(source = "admin.first_name", read_only = True)
    admin_last_name = EmailField(source = "admin.last_name", read_only = True)
    admin_contact = EmailField(source = "admin.contact", read_only = True)
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
    admin_first_name = EmailField(source = "admin.first_name", read_only = True)
    admin_last_name = EmailField(source = "admin.last_name", read_only = True)
    admin_contact = EmailField(source = "admin.contact", read_only = True)
    class Meta:
        model = Department
        fields = "__all__"

class ProjectSerializer(ModelSerializer):
    
    class Meta:
        model = Project
        fields = "__all__"

# pending 
class TaskSummarySerializer(serializers.Serializer):
    date = serializers.DateField()  # The date for daily, weekly, or monthly
    task_count = serializers.IntegerField()  # The count of tasks
    total_duration = serializers.FloatField()  # The total duration of tasks

class EmployeeTaskSummarySerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()  # Employee ID
    employee_name = serializers.CharField()  # Employee name
    department_name = serializers.CharField()  # Department name
    daily_tasks = TaskSummarySerializer(many=True)  # List of daily task summaries
    weekly_tasks = TaskSummarySerializer(many=True)  # List of weekly task summaries
    monthly_tasks = TaskSummarySerializer(many=True)  # List of monthly task summaries

    
# end pending 