from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('tasks/', views.tasks_display, name="tasks"),
    path('report_issue', views.report_issue_view, name="report_issue"),
    path('issues/', views.reported_issues_display, name="reported_issues_display")
]
