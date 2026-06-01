from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),

    # Logout custom
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('guru/', views.teacher_dashboard, name='teacher_dashboard'),
    path('siswa/', views.student_dashboard, name='student_dashboard'),
    path('scan/', views.scan_qr, name='scan_qr'),
    path('plant/<slug:code>/', views.plant_detail, name='plant_detail'),

    path('plants/add/', views.plant_add, name='plant_add'),
    path('plants/<int:pk>/edit/', views.plant_edit, name='plant_edit'),
    path('plants/<int:pk>/delete/', views.plant_delete, name='plant_delete'),

    path('plants/<int:plant_id>/quizzes/', views.quiz_manage, name='quiz_manage'),
    path('plants/<int:plant_id>/quizzes/add/', views.quiz_add, name='quiz_add'),

    path('quizzes/<int:pk>/edit/', views.quiz_edit, name='quiz_edit'),
    path('quizzes/<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),

    path('scores/<int:pk>/delete/', views.score_delete, name='score_delete'),
]