from django.shortcuts import render, redirect
from .forms import CreateEmployee, EmployeeData, MedicineData, VendorData, StockData
from .models import Employee, Medicine, Vendor, MedicineToVendor, Stock
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

import datetime

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
            trade_name = form_med.cleaned_data['trade_name']
            generic_name = form_med.cleaned_data['generic_name']
            unit_sell_price = form_med.cleaned_data['unit_sell_price']
            unit_purchase_price = form_med.cleaned_data['unit_purchase_price']

            m = Medicine(trade_name=trade_name,generic_name=generic_name,unit_sell_price=unit_sell_price,unit_purchase_price=unit_purchase_price)
            m.save()
            id = m.id
            med_id = "MED"+str(id)
            m.medicine_id = med_id
            m.save()
            
            form_med = MedicineData()
            context ={
            'form_med': form_med,
            'med_id': med_id
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

def CreateVendor(request):
    if request.method != 'POST':
        form_ven = VendorData()
        context ={
            'form_ven': form_ven
        }
        return render(request, 'app/create-vendor.html', context)
    else:
        form_ven = VendorData(request.POST)
        if form_ven.is_valid():
            vendor_name = form_ven.cleaned_data['vendor_name']
            email = form_ven.cleaned_data['email']
            mobile = form_ven.cleaned_data['mobile']
            address = form_ven.cleaned_data['address']
            medicine_ids = form_ven.cleaned_data['medicine_ids']

            meds = medicine_ids.split(";")
            for med in meds:
                try:
                    Medicine.objects.get(medicine_id=med)
                except:
                    form_ven = VendorData()
                    context={
                        'form_ven':form_ven,
                        'err': "Medicine_id "+med+" not found"
                    }
                    return render(request, 'app/create-vendor.html', context)

            v = Vendor(vendor_name=vendor_name,mobile=mobile,email=email,address=address, medicine_ids=medicine_ids)
            v.save()
            id = v.id
            ven_id = "VEN"+str(id)
            v.vendor_id = ven_id
            v.save()

            for m in meds:
                k = MedicineToVendor(medicine_id=m, vendor_id=ven_id)
                k.save()
            
            form_ven = VendorData()
            context ={
            'form_ven': form_ven,
            'ven_id': ven_id
            }
            return render(request, 'app/create-vendor.html', context)
        else:
            form_ven = VendorData()
            err = form_ven.errors
            context ={
                'form_ven': form_ven,
                'err': err
            }
            return render(request, 'app/create-medicine.html', context)

def AddStock(request):
    if request.method != 'POST':
        form_stock = StockData()
        context ={
            'form_stock': form_stock
        }
        return render(request, 'app/add-stock.html', context)
    else:
        form_stock = StockData(request.POST)
        if form_stock.is_valid():
            medicine_id = form_stock.cleaned_data['medicine_id']
            batch_id = form_stock.cleaned_data['batch_id']
            quantity = form_stock.cleaned_data['quantity']
            expiry_date = form_stock.cleaned_data['expiry_date']

            try:
                Medicine.objects.get(medicine_id=medicine_id)
            except:
                form_stock = StockData()
                err = medicine_id + " is not valid"
                context ={
                'form_stock': form_stock,
                'err': err
                }
                return render(request, 'app/add-stock.html', context)

            s = Stock(medicine_id=medicine_id, batch_id=batch_id, quantity=quantity, expiry_date=expiry_date)
            s.save()
            
            form_stock = StockData()
            context ={
            'form_stock': form_stock,
            }
            return render(request, 'app/add-stock.html', context)
        else:
            form_stock = StockData()
            err = form_stock.errors
            context ={
                'form_stock': form_stock,
                'err': err
            }
            return render(request, 'app/add-stock.html', context)
            
def TableMedicines(request):
    medicines = Medicine.objects.all()
    context = {
        'medicines': medicines
    }
    return render(request, 'app/all-medicines.html', context)

def TableVendors(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'app/all-vendors.html', context)

def TableEmployees(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    return render(request, 'app/all-employees.html', context)
    
def TableExpired(request):
    all_stock = Stock.objects.all()
    today = datetime.date.today("%y-%m-%d")

    

# Authentication views

def EmployeeLogin(request):
    if request.method == 'POST':
        try:
            if request.session['username']:
                return redirect('index')
        except:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']

                user = authenticate(username=username,password=password)

                if user:
                    if user.is_active:
                        login(request,user)
                        request.session['username'] = username
                        emp = Employee.objects.get(user=user)
                        request.session['is_admin'] = emp.is_admin
                        return redirect('index')
                    else:
                        context = {
                            'err':"Account is inactive"
                        }
                        return render(request, 'registration/login.html', context)
                else:
                    context = {
                        'err':"Invalid credentials"
                    }
                    return render(request, 'registration/login.html', context)
            else:
                return render(request, 'registartion/login.html')
    else:
        return render(request, 'registration/login.html', {})


