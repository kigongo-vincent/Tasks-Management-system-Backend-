from django.urls import path
from . import views


urlpatterns=[
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('companies', views.companies),
    path('company/<str:pk>', views.company),
    path('employee/<str:pk>', views.user),
    path('department/<str:pk>', views.department),
    path('task/<str:pk>', views.task),
    path('company_admins', views.company_admins),
    path('department_admins/<str:pk>', views.department_admins),
    path('departments/<str:pk>', views.departments),
    path('employees/<str:pk>', views.employees),
    path('tasks/<str:pk>', views.tasks),
    path('drafts/<str:pk>', views.drafts),
    path('get_company/<str:pk>', views.get_company),
    path('get_department/<str:pk>', views.get_department),
    path('update_user/<str:pk>', views.update_user),
    path('projects/<str:pk>', views.projects),
    path('project/<str:pk>', views.project),
    path('grouped_tasks/<str:pk>', views.task_grouping, name='grouped'),
    path('task_grouping_by_department/<str:pk>', views.task_grouping_by_department, name='task_grouping_by_department'),
    path('members/<str:pk>', views.company_members),
    path('update_all_tasks/', views.update_all_tasks),
    path('cron_job/', views.cron_job),
    path('backup/', views.export_data_and_send_email),
    path('tasks_logs/<str:pk>', views.logs),
    
]