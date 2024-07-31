from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProjectTasks, Project, ReportIssue
from .forms import ReportIssueForm
from django.shortcuts import redirect

@login_required(login_url='authe:login')
def homepage(request):
    project = Project.objects.all()
    return render(request, 'projects/homepage.html', {'project':project})

def tasks_display(request):
    return render(
        request, 'projects/tasks.html', {'tasks': ProjectTasks.display_tasks()}
    )
    
def report_issue_view(request):
    if request.method == 'POST':
        form = ReportIssueForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            task = form.cleaned_data['task']
            report = form.cleaned_data['report']
            
            task_ = ProjectTasks.objects.create(
                project=project,
                task = task,
                report=report
            )
            task_.save()
            return redirect('projects:reported_issues_display')
    form = ReportIssueForm()
    return render(request, 'projects/report_issue_view.html', {'form':form})
        
def reported_issues_display(request):
    issues = ReportIssue.objects.all()
    return render(
        request, 'projects/reported_issues_display.html', {'issues':issues}
    )