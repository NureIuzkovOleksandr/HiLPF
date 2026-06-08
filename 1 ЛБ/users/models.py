
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('visitor', 'Відвідувач'),
        ('concierge', 'Консьєрж'),
        ('admin', 'Адміністратор'),
    ]

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='visitor',
        verbose_name='Роль користувача'
    )

    is_concierge = models.BooleanField(
        default=False,
        verbose_name='Консьєрж'
    )

    is_admin_user = models.BooleanField(
        default=False,
        verbose_name='Адміністратор'
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата реєстрації'
    )

    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name='Останній вхід'
    )

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_staff_user(self):
        return self.is_concierge or self.is_admin_user

class UserActivityLog(models.Model):

    ACTIVITY_CHOICES = [
        ('login', 'Вхід'),
        ('logout', 'Вихід'),
        ('register', 'Реєстрація'),
        ('update', 'Оновлення'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        verbose_name='Користувач'
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        verbose_name='Тип активності'
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Час'
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP адреса'
    )

    details = models.TextField(
        blank=True,
        verbose_name='Деталі'
    )

    class Meta:
        verbose_name = 'Лог активності'
        verbose_name_plural = 'Логи активності'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} - {self.timestamp}"
