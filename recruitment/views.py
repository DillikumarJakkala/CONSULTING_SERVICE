import csv
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Candidate
from .forms import CandidateSubmissionForm
from .models import User, JobDescription, JobAssignment, Candidate

def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN':
        return redirect('admin_dashboard')
    return redirect('subvendor_dashboard')

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN':
            return redirect('admin_dashboard')
        return redirect('subvendor_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or getattr(user, 'role', '') == 'ADMIN':
                return redirect('admin_dashboard')
            return redirect('subvendor_dashboard')
        else:
            return render(request, 'recruitment/login.html', {'error': 'Invalid username or password'})

    return render(request, 'recruitment/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'):
        return redirect('subvendor_dashboard')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        new_status = request.POST.get('status')
        if candidate_id and new_status:
            candidate = get_object_or_404(Candidate, id=candidate_id)
            candidate.status = new_status
            candidate.save()
            return redirect('admin_dashboard')

    candidates = Candidate.objects.all().select_related('job', 'submitted_by')

    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search_query:
        candidates = candidates.filter(
            Q(candidate_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    if status_filter:
        candidates = candidates.filter(status=status_filter)

    context = {
        'candidates': candidates,
        'search_query': search_query,
        'selected_status': status_filter,
    }
    return render(request, 'recruitment/admin_dashboard.html', context)

@login_required
def subvendor_dashboard(request):
    candidates = Candidate.objects.filter(submitted_by=request.user)
    return render(request, 'recruitment/subvendor_dashboard.html', {'candidates': candidates})

@login_required
def add_candidate(request):
    if request.method == 'POST':
        form = CandidateSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.submitted_by = request.user
            candidate.status = 'SUBMITTED'
            candidate.save()
            return redirect('subvendor_dashboard')
    else:
        form = CandidateSubmissionForm()
    
    return render(request, 'recruitment/add_candidate.html', {'form': form})

@login_required
def update_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    
    if request.method == 'POST':
        candidate.candidate_name = request.POST.get('candidate_name', candidate.candidate_name)
        candidate.email = request.POST.get('email', candidate.email)
        candidate.phone = request.POST.get('phone', candidate.phone)
        if 'status' in request.POST:
            candidate.status = request.POST.get('status')
        candidate.save()
        return redirect('admin_dashboard')

    return render(request, 'recruitment/update_candidate.html', {'candidate': candidate})

@login_required
def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        candidate.delete()
        return redirect('admin_dashboard')
    return render(request, 'recruitment/delete_candidate.html', {'candidate': candidate})

@login_required
def export_candidates_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidates_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Name', 'Email', 'Phone', 'Job Title', 
        'Submitted By', 'Status', 'Submitted Date'
    ])

    if request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN':
        candidates = Candidate.objects.all()
    else:
        candidates = Candidate.objects.filter(submitted_by=request.user)

    for candidate in candidates:
        writer.writerow([
            candidate.id,
            getattr(candidate, 'candidate_name', ''),
            getattr(candidate, 'email', ''),
            getattr(candidate, 'phone', ''),
            str(getattr(candidate, 'job', '')),
            str(getattr(candidate, 'submitted_by', '')),
            getattr(candidate, 'status', ''),
            candidate.created_at.strftime('%Y-%m-%d') if hasattr(candidate, 'created_at') else ''
        ])

    return response


# recruitment/views.py

@login_required
def add_candidate(request):
    if request.method == 'POST':
        # ... your save candidate logic ...
        pass
    else:
        # Show only jobs assigned to the logged-in subvendor
        assigned_jobs = JobDescription.objects.filter(jobassignment__vendor=request.user)
        return render(request, 'recruitment/add_candidate.html', {'jobs': assigned_jobs})