from django.shortcuts import render, redirect
from . import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


def HomePage(request):
    return render(request, 'app/index.html')


def CreateUser(request):
    # form_user = forms.CreateEmployee()
    # form_data = forms.EmployeeData()
    # context = {
    #     'form_data': form_data,
    #     'form_user': form_user
    # }
    # return render(request, 'registration/create-user.html', context)
    if request.method != 'POST':
        form_user = forms.CreateEmployee()
        form_data = forms.EmployeeData()
        context = {
            'form_data': form_data,
            'form_user': form_user
        }
        return render(request, 'registration/create-user.html', context)

    else:
        user_form = forms.CreateEmployee(request.POST)
        employee_data_form = forms.EmployeeData(request.POST)
        if user_form.is_valid() and employee_data_form.is_valid():
            user = user_form.save()
            employee_data = employee_data_form.save(commit=False)
            user.set_password(employee_data.password)
            user.save()
            password = 0
            employee_data.user = user
            employee_data.save()
        else:
            form_user = forms.CreateEmployee()
            form_data = forms.EmployeeData()
            err1 = user_form.errors
            err2 = employee_data_form.errors
            context = {
                'form_data': form_data,
                'form_user': form_user,
                'err1': err1,
                'err2': err2
            }
            return render(request, 'registration/create-user.html', context)
