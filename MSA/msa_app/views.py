from django.shortcuts import render, redirect
from .forms import CreateEmployee, EmployeeData, MedicineData, RevenueProfit, VendorData, StockData
from .models import Employee, ExpiredMedicines, Medicine, MedicineStock, Sales, Vendor, MedicineToVendor, Stock
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

            try:
                t = Medicine.objects.get(generic_name=generic_name)
                form_med = MedicineData()
                context = {
                    'form_med':form_med,
                    'err':"Medicine " + generic_name+" already exists"
                }
                return render(request, 'app/create-medicine.html', context)
            except:
                m = Medicine(trade_name=trade_name,generic_name=generic_name,unit_sell_price=unit_sell_price,unit_purchase_price=unit_purchase_price)
                m.save()
                id = m.id
                med_id = "MED"+str(id)
                m.medicine_id = med_id
                m.save()

                ms = MedicineStock(medicine_id=med_id)
                ms.save()
                
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

            try:
                d = Vendor.objects.get(email=email)
                form_ven = VendorData()
                context = {
                    'form_ven':form_ven,
                    'err':"Vendor data already exists"
                }
                return render(request, 'app/create-vendor.html', context)
            except:
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
            vendor_id = form_stock.cleaned_data['vendor_id']

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
            
            try:
                Vendor.objects.get(vendor_id=vendor_id)
            except:
                form_stock = StockData()
                err = vendor_id + " is not valid"
                context = {
                    'form_stock': form_stock,
                    'err': err
                }
                return render(request, 'app/add-stock.html', context)

            s = Stock(medicine_id=medicine_id, batch_id=batch_id, quantity=quantity, expiry_date=expiry_date, vendor_id=vendor_id)
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
    today = datetime.date.today()

    expired = []

    for stock in all_stock:
        if stock.expiry_date <= today:
            med_id = stock.medicine_id
            ven_id = stock.vendor_id
            batch_id = stock.batch_id
            ms = MedicineStock.objects.get(medicine_id = stock.medicine_id)
            available_stock = ms.stock - stock.quantity
            v = Vendor.objects.get(vendor_id = stock.vendor_id)
            ven_email = v.email
            ven_address = v.address
            expired.append({
                'med_id': med_id,
                'ven_id':ven_id,
                'batch_id':batch_id,
                'available_stock':available_stock,
                'ven_email':ven_email,
                'ven_address':ven_address
            })
            e = ExpiredMedicines(medicine_id = med_id, quantity = stock.quantity)
            e.save()
    
    context = {
        'expired_meds': expired
    }
    return render(request, 'app/expired-medicines.html', context)

def TablePurchase(request):
    all_meds_stock = MedicineStock.objects.all()
    
    purchase = []

    for med in all_meds_stock:
        if med.stock <= med.threshold:
            med_id = med.medicine_id
            stock = med.stock
            threshold = med.threshold
            v = MedicineToVendor.objects.filter(medicine_id=med_id).first()
            ven_id = v.vendor_id
            v_info = Vendor(vendor_id=ven_id)
            number = v_info.number
            email = v_info.email
            address = v_info.address
            purchase.append({
                'med_id':med_id,
                'stock':stock,
                'threshold':threshold,
                'ven_id':ven_id,
                'number':number,
                'email':email,
                'address':address
            })

    context = {
        'purchase':purchase
    }

    return render(request, 'app/purchase-table.html', context)

def RevenueProfitView(request):
    if request.method == 'POST':
        form = RevenueProfit(request.POST)
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']

        if to_date <= from_date:
            context={
                'form': RevenueProfit(),
                'err': "To date should be after from date"
            }
            return render(request, 'app/revenue-profit.html', context)

        sales = Sales.objects.all()
        expired = ExpiredMedicines.objects.all()

        revenue = profit = 0
        try:
            for sale in sales:
                if sale.date > from_date and sale.date < to_date:
                    sp = Medicine.objects.get(medicine_id=sale.medicine_id)
                    cp = Medicine.objects.get(medicine_id=sale.medicine_id)
                    revenue += sp*sale.quantity
                    profit += (sp-cp)*sale.quantity
            
            for med in expired:
                if med.expiry_date > from_date and med.expiry_date < to_date:
                    cp = Medicine.objects.get(medicine_id=med.medicine_id)
                    profit -= med.quantity*cp

            form = RevenueProfit()
            context={
                'form':form,
                'revenue':revenue,
                'profit':profit
            }
            return render(request, 'app/revenue-profit.html', context)
        except:
            context={
                'form':form,
                'err':"Some error occured"
            }
            return render(request, 'app/revenue-profit.html', context)
    else:
        form = RevenueProfit()
        return render(request, 'app/revenue-profit.html', {'form':form})


# edit stuff

def EditMedicine(request, id):
    if request.method == 'POST':
        form = MedicineData(request.POST)
        if form.is_valid():
            trade_name = form.cleaned_data['trade_name']
            generic_name = form.cleaned_data['generic_name']
            unit_sell_price = form.cleaned_data['unit_sell_price']
            unit_purchase_price = form.cleaned_data['unit_purchase_price']

            m = Medicine.objects.get(medicine_id=id)
            m.trade_name = trade_name
            m.generic_name = generic_name
            m.unit_sell_price = unit_sell_price
            m.unit_purchase_price = unit_purchase_price
            m.save()

            return redirect('/app/allmedicines')

        else:
            form = MedicineData()
            context = {
                'form':form,
                'err': form.errors,
                'id':id
            }
            return render(request, 'app/edit-medicine.html',context)
    else:
        form = MedicineData()
        context = {
            'form':form,
            'id':id
        }
        return render(request, 'app/edit-medicine.html', context)

def EditVendor(request, id):
    if request.method == 'POST':
        form = VendorData(request.POST)
        if form.is_valid():
            vendor_name = form.cleaned_data['vendor_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            address = form.cleaned_data['address']
            medicine_ids = form.cleaned_data['medicine_ids']

            meds = medicine_ids.split(";")
            for med in meds:
                try:
                    Medicine.objects.get(medicine_id=med)
                except:
                    form_ven = VendorData()
                    context={
                        'form':form,
                        'err': "Medicine ID "+med+" not found",
                        'id':id
                    }
                    return render(request, 'app/edit-vendor.html', context)            

            v = Vendor.objects.get(vendor_id=id)
            v.vendor_name = vendor_name
            v.email = email
            v.mobile = mobile
            v.address = address
            v.medicine_ids = medicine_ids
            v.save()

            MedicineToVendor.objects.filter(vendor_id=id).delete()

            for m in meds:
                k = MedicineToVendor(medicine_id=m,vendor_id=id)
                k.save()

            return redirect('/app/allvendors')

        else:
            form = VendorData()
            context = {
                'form':form,
                'err': form.errors,
                'id':id
            }
            return render(request, 'app/edit-vendor.html',context)
    else:
        form = VendorData()
        context = {
            'form':form,
            'id':id
        }
        return render(request, 'app/edit-vendor.html', context)

def EditEmployee(request, id):
    if request.method == 'POST':
        user_form = CreateEmployee(request.POST)
        employee_data_form = EmployeeData(request.POST)
        if user_form.is_valid() and employee_data_form.is_valid():
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

            prev = Employee.objects.get(id = id).user
            prev_user = User.objects.get(username=prev.username)
            prev_user.delete()

            u = User(username=username, email=email)
            u.set_password(password)
            u.save()
            e = Employee(user=u, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth,
                        gender=gender, phone=phone, address=address, is_admin=is_admin, password=password, confirm_password=confirm_password)
            e.save()
            return redirect('/app/allemployees') 
        else:
            form_user = CreateEmployee()
            form_data = EmployeeData()
            err1 = user_form.errors
            err2 = employee_data_form.errors
            context = {
                'form_data': form_data,
                'form_user': form_user,
                'err1': err1,
                'err2': err2,
                'id':id
            }
            return render(request, 'app/edit-employee.html', context)
    else:
        form_user = CreateEmployee()
        form_data = EmployeeData()
        context = {
            'form_user':form_user,
            'form_data':form_data,
            'id':id
        }
        return render(request, 'app/edit-employee.html', context)


        
        

# Authentication views

def EmployeeLogin(request):
    if request.method == 'POST':
        try:
            if request.session['username']:
                return render(request, 'registration/index.html', {})
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
                        return render(request, 'registration/index.html', {})
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


