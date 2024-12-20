from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from issues.views import submit_issue, issue_list, admin_dashboard

 
urlpatterns = [
    
    path('', submit_issue, name='issue_submit'),
    path('admin/', admin.site.urls),
    path('issues/', issue_list, name='issue_list'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)