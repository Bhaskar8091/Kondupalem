from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Issue, IssueFile
from .forms import IssueForm
from django.db.models import Q

def submit_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)

        if form.is_valid():
            issue = form.save()
            
            # Handle multiple file uploads
            files = request.FILES.getlist('files')
            for file in files:
                IssueFile.objects.create(issue=issue, file=file)
            
            # Send email notification to admin
           
            # send_mail(
            #                 'New Issue Submitted',
            #                     f'New issue submitted by {issue.username}\nSubject: {issue.subject}',
            #                     settings.EMAIL_HOST_USER,
            #                     fail_silently=False,
            #             )      
            
            messages.success(request, 'Issue submitted successfully!')
            return redirect('issue_list')
        
    else:
        form = IssueForm()
        
    
    return render(request, 'issues/submit_issue.html', {'form': form})

def issue_list(request):
    pending_issues = Issue.objects.filter(status='pending')
    accepted_issues = Issue.objects.filter(status='accepted')
    rejected_issues = Issue.objects.filter(status='rejected')
    completed_issues = Issue.objects.filter(status='completed')

    return render(request, 'issues/issue_list.html', {
        'pending_issues': pending_issues,
        'accepted_issues': accepted_issues,
        'rejected_issues': rejected_issues,
        'completed_issues': completed_issues,
    })

def accept_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.accept()
    messages.success(request, 'Issue accepted successfully!')
    return redirect('admin_dashboard')

def reject_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.reject()
    messages.success(request, 'Issue rejected successfully!')
    return redirect('admin_dashboard')

def complete_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.complete()
    messages.success(request, 'Issue completed successfully!')
    return redirect('admin_dashboard')

def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('issue_list')

    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        action = request.POST.get('action')

        if not issue_id or not action:
            messages.error(request, 'Invalid request.')
            return redirect('admin_dashboard')

        try:
            issue = Issue.objects.get(id=int(issue_id))
        except (ValueError, Issue.DoesNotExist):
            messages.error(request, 'Invalid issue ID.')
            return redirect('admin_dashboard')

        if action == 'accept':
            issue.accept()
            issue.save()
            messages.success(request, 'Issue accepted successfully!')
        elif action == 'reject':
            issue.reject()
            issue.save()
            messages.success(request, 'Issue rejected successfully!')
        elif action == 'complete':
            issue.complete()
            issue.save()
            messages.success(request, 'Issue completed successfully!')
        elif action == 'delete':
            issue.delete()
            messages.success(request, 'Issue deleted successfully!')
        return redirect('admin_dashboard')

    issues = Issue.objects.all().order_by('-created_at')
    pending_issues = Issue.objects.filter(status='pending')
    accepted_issues = Issue.objects.filter(status='accepted')
    rejected_issues = Issue.objects.filter(status='rejected')
    completed_issues = Issue.objects.filter(status='completed')
    query = request.GET.get('q')
    if query:
        issues = issues.filter(
            Q(username__icontains=query) |
            Q(subject__icontains=query) |
            Q(created_at__icontains=query)
        )

    return render(request, 'issues/admin_dashboard.html', {
        'pending_issues': pending_issues,
        'accepted_issues': accepted_issues,
        'rejected_issues': rejected_issues,
        'completed_issues': completed_issues,
        'issues': issues
    })

