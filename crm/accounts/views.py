from django.shortcuts import render, redirect
from accounts.forms import *
from accounts.models import User, Role
# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    print('1')
    if request.user.is_authenticated:
        # for different roles
        pass
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

            return redirect('/home')

    return render(request, 'register.html', args)
