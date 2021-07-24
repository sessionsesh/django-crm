from django import forms
from accounts.models import User, Role


class UserRegisterForm(forms.Form):
    email = forms.CharField()
    email.widget = forms.TextInput(attrs={'type': 'email', 'id': 'inputEmail', 'class': 'form-control',
                                   'placeholder': 'Email', 'required': True, 'autofocus': True})
    username = forms.CharField()
    username.widget = forms.TextInput(attrs={'type': 'username', 'id': 'inputUsername',
                                      'class': 'form-control', 'placeholder': 'Логин', 'required': True, 'autofocus': False})
    password = forms.CharField()
    password.widget = forms.PasswordInput(attrs={'type': 'password', 'id': 'inputPassword',
                                          'class': 'form-control', 'placeholder': 'Пароль', 'required': True, 'autofocus': False})
    confirm_password = forms.CharField()
    confirm_password.widget = forms.PasswordInput(attrs={'type': 'password', 'id': 'inputConfirmPassword',
                                                  'class': 'form-control', 'placeholder': 'Подтверждение пароля', 'required': True, 'autofocus': False})

    role = forms.CharField()
    role.widget = forms.Select(choices=Role.choices, attrs={'type': 'role', 'id': 'role',
                                                            'class': 'form-control', 'placeholder': 'Выбор роли', 'required': True, 'autofocus': False})

    help_texts = {'email': None, 'username': None,
                  'password': None, 'role': None}

    def clean(self):
        super(UserRegisterForm, self).clean()
        # Check username busyness
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("This username is already taken")

        # Check email busyness
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is already taken")

        # Check password matching
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords doesn\'t match')

        # Delete confirm password from form just not to override save() method
        del self.cleaned_data['confirm_password']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    username.widget = forms.TextInput(attrs={'type': 'text', 'id': 'inputUsername',
                                      'class': 'form-control', 'placeholder': 'Логин', 'required': True, 'autofocus': True})

    password = forms.CharField()
    password.widget = forms.PasswordInput(
        attrs={'type': 'password', 'id': 'inputPassword', 'class': 'form-control', 'placeholder': 'Пароль', 'required': True})

    def clean(self):
        super(UserLoginForm, self).clean()
        if not User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(
                "Wrong username")
