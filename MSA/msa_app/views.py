from django.shortcuts import render, redirect
from .forms import CreateEmployee, EmployeeData, MedicineData 
from .models import Employee
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
        form_user = CreateEmployee()
        form_data = EmployeeData()
        context = {
            'form_data': form_data,
            'form_user': form_user
        }
        return render(request, 'registration/create-user.html', context)
    else:
        user_form = CreateEmployee(request.POST)
        employee_data_form = EmployeeData(request.POST)
        if user_form.is_valid() and employee_data_form.is_valid():
            # user = user_form.save()
            # employee_data = employee_data_form.save(commit=False)
            # user.set_password(employee_data.password)
            # user.save()
            # password = 0
            # employee_data.user = user
            # employee_data.save()
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            first_name = employee_data_form.cleaned_data['first_name']
            middle_name = employee_data_form.cleaned_data['middle_name']
            last_name = employee_data_form.cleaned_data['last_name']
            date_of_birth = employee_data_form.cleaned_data['date_of_birth']
            gender = employee_data_form.cleaned_data['gender']
            phone = employee_data_form.cleaned_data['phone']
            address = employee_data_form.cleaned_data['address']
            is_admin = employee_data_form.cleaned_data['is_admin']
            password = employee_data_form.cleaned_data['password']
            confirm_password = employee_data_form.cleaned_data['confirm_password']
            u = User(username=username, email=email)
            u.set_password(password)
            u.save()
            e = Employee(user=u, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth,
                        gender=gender, phone=phone, address=address, is_admin=is_admin, password=password, confirm_password=confirm_password)
            e.save()
            form_user = CreateEmployee()
            form_data = EmployeeData()
            context = {
            'form_data': form_data,
            'form_user': form_user
            }
            return render(request, 'registration/create-user.html', context) 
        else:
            form_user = CreateEmployee()
            form_data = EmployeeData()
            err1 = user_form.errors
            err2 = employee_data_form.errors
            context = {
                'form_data': form_data,
                'form_user': form_user,
                'err1': err1,
                'err2': err2
            }
            return render(request, 'registration/create-user.html', context)

def CreateMedicine(request):
    if request.method != 'POST':
        form_med = MedicineData()
        context ={
            'form_med': form_med
        }
        return render(request, 'app/create-medicine.html', context)
    else:
        form_med = MedicineData(request.POST)
        if form_med.is_valid():
            form_med.save()
             
            form_med = MedicineData()
            context ={
            'form_med': form_med
            }
            return render(request, 'app/create-medicine.html', context)
        else:
            form_med = MedicineData()
            err = form_med.errors
            context ={
                'form_med': form_med,
                'err': err
            }
            return render(request, 'app/create-medicine.html', context)
            