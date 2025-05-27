from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Logger)
