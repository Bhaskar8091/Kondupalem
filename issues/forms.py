from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        help_text='Upload images, PDFs, or text files related to your issue'
    )
    
    class Meta:
        model = Issue
        fields = ['username', 'subject','matter']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'subject': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'matter': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
        }