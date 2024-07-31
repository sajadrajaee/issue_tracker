from django.db import models
from authe.models import CustomUser
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_detail = models.TextField()
    time_to_start = models.DateField(auto_now_add=True)
    time_to_finish = models.DateField(default=None)
    image = models.ImageField(
        upload_to = 'projects/images/',
        null=True,
        blank=True,
        default=None
    )
    
    def __str__(self):
        return self.project_name
    
class ProjectTasks(models.Model):
    
    class Meta:
        verbose_name = "project's tasks"
        verbose_name_plural = "project's tasks"
        
    task_choices = (
        ('free', 'free'),
        ('working_on', 'working on'),
        ('done', 'done')
    )
    title = models.CharField(max_length=59)
    content = models.CharField(max_length=300, default=None)

    assigned_to = models.ForeignKey(
        CustomUser, verbose_name=_("assigned to"), 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    time_to_finish = models.DateField(verbose_name=_("time to finish"), default=None)
    
    task_status = models.CharField(
        max_length=10,
        choices=task_choices
    )
    image = models.ImageField(
        upload_to = 'projects/images/',
        null=True,
        blank=True,
        default=None
    ) 
    
    def __str__(self):
        return f"{self.title} | {self.task_status}"
    
    def display_tasks():
        return ProjectTasks.objects.all()

class ReportIssue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(ProjectTasks, on_delete=models.CASCADE)
    report = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.report[:20]
    