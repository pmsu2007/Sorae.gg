from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from common.forms import *


def signup(request):
    """
    create user account
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('community:list', category='all')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


class PasswordResetView(auth_views.PasswordResetView):
    """
    reset password : input user's email
    """
    template_name = 'common/password_reset.html'
    success_url = reverse_lazy('common:password_reset_done')
    form_class = PasswordResetForm



class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    reset password : sending email
    """
    template_name = 'common/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    reset password : input new password
    """
    template_name = 'common/password_reset_confirm.html'
    success_url = reverse_lazy('common:login')
