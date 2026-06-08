
from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        })
    )

    password_confirm = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть пароль'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ім\'я користувача'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ім\'я'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Прізвище'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+38 (0ХХ) XXX-XX-XX'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')


        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Паролі не збігаються.')


        if password and len(password) < 8:
            raise forms.ValidationError('Пароль повинен містити мінімум 8 символів.')

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Це ім\'я користувача вже зареєстровано.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже зареєстрований.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):

    username = forms.CharField(
        label='Ім\'я користувача',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ім\'я користувача',
            'autofocus': True
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        })
    )

    remember_me = forms.BooleanField(
        label='Запам\'ятати мене',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ім\'я'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Прізвище'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон'
            }),
        }

class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        label='Старий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть старий пароль'
        })
    )

    new_password = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть новий пароль'
        })
    )

    new_password_confirm = forms.CharField(
        label='Підтвердження нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть новий пароль'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        if new_password and new_password_confirm:
            if new_password != new_password_confirm:
                raise forms.ValidationError('Нові паролі не збігаються.')

        if new_password and len(new_password) < 8:
            raise forms.ValidationError('Пароль повинен містити мінімум 8 символів.')

        return cleaned_data
