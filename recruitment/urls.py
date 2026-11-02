from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('subvendor-dashboard/', views.subvendor_dashboard, name='subvendor_dashboard'),
    path('subvendor/add-candidate/', views.add_candidate, name='add_candidate'),  # <--- Make sure this line is here!
    path('export-candidates/', views.export_candidates_csv, name='export_candidates_csv'),
    path('candidate/<int:pk>/update/', views.update_candidate, name='update_candidate'),
    path('candidate/<int:pk>/delete/', views.delete_candidate, name='delete_candidate'),
]