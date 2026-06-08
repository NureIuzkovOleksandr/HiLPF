from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import CustomUser, UserActivityLog
from .forms import UserRegistrationForm, UserLoginForm

class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                UserActivityLog.objects.create(
                    user=user,
                    activity_type='register',
                    ip_address=self._get_client_ip(request),
                    details='Користувач зареєстрований'
                )
                messages.success(
                    request,
                    f'Вітаємо, {user.username}! Ви успішно зареєстровані. Можете увійти.'
                )
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f'Помилка реєстрації: {str(e)}')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                UserActivityLog.objects.create(
                    user=user,
                    activity_type='login',
                    ip_address=self._get_client_ip(request),
                    details='Успішний вхід'
                )
                messages.success(request, f'Добро пожалувати, {user.username}!')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Невірне ім\'я користувача або пароль')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        UserActivityLog.objects.create(
            user=request.user,
            activity_type='logout',
            ip_address=self._get_client_ip(request),
            details='Користувач вийшов'
        )
        logout(request)
        messages.success(request, 'Ви успішно вийшли з системи.')
        return redirect('users:login')

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class DashboardView(LoginRequiredMixin, View):
    template_name = 'users/dashboard.html'
    login_url = 'users:login'

    def get(self, request):
        user = request.user
        activity_logs = UserActivityLog.objects.filter(user=user)[:10]
        context = {
            'user': user,
            'activity_logs': activity_logs,
            'role_display': user.get_role_display(),
            'is_staff': user.is_staff_user(),
        }
        return render(request, self.template_name, context)

class AdminPanelView(LoginRequiredMixin, View):
    template_name = 'users/admin_panel.html'
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin_user:
            messages.error(request, 'У вас немає прав доступу до цієї сторінки.')
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = CustomUser.objects.all()
        activity_logs = UserActivityLog.objects.all()[:50]
        context = {
            'users': users,
            'activity_logs': activity_logs,
            'total_users': users.count(),
            'concierges': users.filter(is_concierge=True).count(),
            'admins': users.filter(is_admin_user=True).count(),
        }
        return render(request, self.template_name, context)
