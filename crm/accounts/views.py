from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.forms import *
from accounts.models import User, Role
# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    print('1')
    if request.user.is_authenticated:
        redirect('/orders')

    print('2')
    args = {}
    if request.method == 'GET':
        print('3')
        reg_form = UserRegisterForm()
        args['reg_form'] = reg_form
    if request.method == 'POST':
        data = request.POST
        reg_form = UserRegisterForm(data=data)
        args = {'reg_form': reg_form}
        if reg_form.is_valid():
            if (data['role'] == Role.EMP):
                User.objects.create_employee(**reg_form.cleaned_data)

            if (data['role'] == Role.CUS):
                User.objects.create_customer(**reg_form.cleaned_data)

            if (data['role'] == Role.ADM):
                User.objects.create_admin(**reg_form.cleaned_data)

            return redirect('/login')

    return render(request, 'register.html', args)


def login_(request):
    if request.user.is_authenticated:
        redirect('/orders')

    args = {}
    if request.method == 'GET':
        args['log_form'] = UserLoginForm()
    if request.method == 'POST':
        data = request.POST
        log_form = UserLoginForm(data=data)
        args['log_form'] = log_form
        if log_form.is_valid():
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username,
                                password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('/orders')
    # else
    return render(request, 'login.html', args)


@login_required
def logout_(request):
    logout(request)
    return redirect('/login')
