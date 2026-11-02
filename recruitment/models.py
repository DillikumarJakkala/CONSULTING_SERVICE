from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SUBVENDOR', 'Subvendor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SUBVENDOR')
    company_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class JobDescription(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('ON_HOLD', 'On Hold'),
    )
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True, null=True)
    no_of_positions = models.PositiveIntegerField(default=1)
    target_dates = models.DateField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobAssignment(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'SUBVENDOR'})
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title} -> {self.vendor.username}"

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted by Subvendor'),
        ('AGENCY_REVIEW', 'Company A Review'),
        ('SUBMITTED_TO_CLIENT', 'Submitted to Client'),
        ('CLIENT_SHORTLISTED', 'Client Shortlisted'),
        ('INTERVIEW', 'Interview Stage'),
        ('OFFERED', 'Offer Released'),
        ('JOINED', 'Joined (Hired)'),
        ('REJECTED', 'Rejected'),
        ('ON_HOLD', 'On Hold'),
    ]

    candidate_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} ({self.job.title})"