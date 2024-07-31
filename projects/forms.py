from django import forms
from .models import ReportIssue

class ReportIssueForm(forms.ModelForm):
    
    class Meta:
        model = ReportIssue
        exclude = ('report_date',)