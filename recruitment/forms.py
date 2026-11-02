from django import forms
from .models import Candidate

class CandidateSubmissionForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['candidate_name', 'email', 'phone', 'job', 'resume']
        widgets = {
            'candidate_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'job': forms.Select(attrs={'class': 'form-select'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }