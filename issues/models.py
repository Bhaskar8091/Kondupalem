from django.db import models
from django.utils import timezone
import os

def get_upload_path(instance, filename):
    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
    return os.path.join('issues', instance.issue.username, timestamp, filename)


class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    username = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    matter = models.TextField(max_length=300,null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.subject}"

    def accept(self):
        self.status = 'accepted'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

    def complete(self):
        self.status = 'completed'
        self.save()

# class Issue(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     ]
    
#     username = models.CharField(max_length=100)
#     subject = models.CharField(max_length=200)
#     matter=models.TextField(max_length=300)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.username} - {self.subject}"

# class IssueFile(models.Model):
#     issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='files')
#     file = models.FileField(upload_to=get_upload_path)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.issue.username} - {self.file.name}"
# class IssueFile(models.Model):
#     issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='files')
#     file = models.FileField(upload_to=get_upload_path)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.issue.username} - {self.file.name}"
class IssueFile(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue} - {self.file.name}"