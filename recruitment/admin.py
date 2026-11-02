from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobDescription, JobAssignment, Candidate

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'company_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company_name')}),
    )
    
@admin.action(description='Assign selected jobs to all active Subvendors')
def assign_to_subvendors(modeladmin, request, queryset):
    subvendors = User.objects.filter(role='SUBVENDOR')
    created_count = 0
    for job in queryset:
        for vendor in subvendors:
            _, created = JobAssignment.objects.get_or_create(job=job, vendor=vendor)
            if created:
                created_count += 1
    modeladmin.message_user(request, f"Successfully created {created_count} job assignments.")

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'no_of_positions', 'target_dates', 'status', 'created_at')
    search_fields = ('title', 'location', 'skills')
    actions = [assign_to_subvendors]
    
@admin.register(JobAssignment)
class JobAssignmentAdmin(admin.ModelAdmin):
    list_display = ('job', 'vendor', 'assigned_at')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'job', 'submitted_by', 'status', 'submitted_at')
    list_filter = ('status', 'job', 'submitted_by')
    search_fields = ('candidate_name', 'email', 'phone')

admin.site.register(User, CustomUserAdmin)