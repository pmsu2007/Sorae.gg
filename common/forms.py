from django import forms
import django.contrib.auth.forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(auth_forms.UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class PasswordResetForm(auth_forms.PasswordResetForm):
    username = auth_forms.UsernameField(label="사용자 ID")
    """
    validation 절차
    1. username에 대응하는 User 인스턴스가 존재하는지 확인
    2. username에 대응하는 email과 입력받은 email이 동일한지 확인
    """
    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise ValidationError("해당 사용자가 존재하지 않습니다.")

        return data

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        if username and email:
            if User.objects.get(username=username).email != email:
                raise ValidationError("입력한 이메일 주소와 사용자의 이메일 주소가 일치하지 않습니다.")

    def get_users(self, email):
        active_users = User.objects.filter(**{
            'username__iexact': self.cleaned_data["username"],
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password()
        )