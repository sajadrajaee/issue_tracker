from django.db import models
from authe.models import CustomUser

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_detail = models.TextField()
    project_doer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    time_to_start = models.DateField(auto_now_add=True)
    time_to_finish = models.DateField(default=None)
    
    def __str__(self):
        return self.project_name
    
