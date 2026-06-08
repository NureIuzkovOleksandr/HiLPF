
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('admin-panel/', views.AdminPanelView.as_view(), name='admin_panel'),
]
