from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# customizing the default user model 
class User(AbstractUser):
    username = models.CharField(unique=True, null=True, blank=True, max_length=100)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=100, default="admin")
    contact = models.CharField(max_length=15, null=True, blank=True) 
    department = models.ForeignKey("base.Department", on_delete=models.SET_NULL, null=True, blank = True)
    REQUIRED_FIELDS=['username'] # must be added to avoid complications when creating the super user
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["-date_joined"]


class Task(models.Model):
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)    
    updated_at = models.DateField(auto_now=True)    
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.DecimalField(decimal_places=2, max_digits=1000)
    project = models.ForeignKey("base.Project", on_delete=models.SET_NULL, null = True, blank = True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.body[0:20]

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_admin")
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="department_admin")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null =True, blank = True)
    
    
    def __str__(self):
        return self.name