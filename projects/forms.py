from django import forms
from .models import ReportIssue

class ReportIssueForm(forms.ModelForm):
    
    class Meta:
        model = ReportIssue
        fields = ('project', 'task', 'report')