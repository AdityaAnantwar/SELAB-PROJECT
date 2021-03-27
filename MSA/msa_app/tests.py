from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from .forms import CreateEmployee, EmployeeData, VendorData, MedicineData, VendorData, StockData, SalesData
from .models import Medicine, Stock, Sales, Vendor
from django.contrib.auth.models import User

# forms testing

class EmployeeDataFormTest(TestCase):
    def test_mobile_number_digits_not_ten(self):
        user = CreateEmployee(data = {'username':"testuser", 'email':"test@test.com", 'password': "adminpass"})
        form = EmployeeData(data={'user':user,
                                'first_name':"test_first",
                                'middle_name':"test_middle",
                                'last_name':"test_last",
                                'date_of_birth':datetime.date.today()-datetime.timedelta(years=19),
                                'gender':"Male",
                                'phone': 12345678,
                                'address': "some address",
                                'is_admin': True,
                                'password':"adminpass",
                                'confirm_password':"adminpass"})
        self.assertFalse(form.is_valid())
    
    def test_mobile_number_digits_ten(self):
        user = CreateEmployee(data = {'username':"testuser", 'email':"test@test.com", 'password': "adminpass"})
        form = EmployeeData(data={'user':user,
                                'first_name':"test_first",
                                'middle_name':"test_middle",
                                'last_name':"test_last",
                                'date_of_birth':datetime.date.today()-datetime.timedelta(years=19),
                                'gender':"Male",
                                'phone': 1234567890,
                                'address': "some address",
                                'is_admin': True,
                                'password':"adminpass",
                                'confirm_password':"adminpass"})
        self.assertTrue(form.is_valid())
        
class VendorDataFormTest(TestCase):
    def test_mobile_number_digits_not_ten(self):
        form = VendorData(data={'vendor_name':"test name",
                                'email': "test@test.com",
                                'mobile': 12345678,
                                'address': "test address",
                                'medicine_ids':"MED1;MED5"})
        
        self.assertFalse(form.is_valid())

    def test_mobile_number_digits_ten(self):
        form = VendorData(data={'vendor_name':"test name",
                                'email': "test@test.com",
                                'mobile': 1234567890,
                                'address': "test address",
                                'medicine_ids':"MED1;MED5"})
        
        self.assertTrue(form.is_valid())

class SalesDataFormTest(TestCase):
    def quantity_negative(self):
        form = SalesData(data={'medicine_id': "MED2",
                            'quantity': -3})
        self.assertFalse(form.is_active())
    
    def quantity_positive(self):
        form = SalesData(data={'medicine_id': "MED2",
                            'quantity': 3})
        self.assertFalse(form.is_active())

class StockDataFormTest(TestCase):
    def quantity_negative(self):
        form = StockData(data={'medicine_id':"MED4",
                                'batch_id':"sample batch id",
                                'quantity': -3,
                                'expiry_date': datetime.date.today() + datetime.timedelta(week=1)})
        self.assertFalse(form.is_valid())
    
    def quantity_postive(self):
        form = StockData(data={'medicine_id':"MED4",
                                'batch_id':"sample batch id",
                                'quantity': 3,
                                'expiry_date': datetime.date.today() + datetime.timedelta(week=1)})
        self.assertTrue(form.is_valid())

    def expiry_date_before_today(self):
        form = StockData(data={'medicine_id':"MED4",
                                'batch_id':"sample batch id",
                                'quantity': 3,
                                'expiry_date': datetime.date.today() - datetime.timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def expiry_date_after_today(self):
        form = StockData(data={'medicine_id':"MED4",
                                'batch_id':"sample batch id",
                                'quantity': 3,
                                'expiry_date': datetime.date.today() + datetime.timedelta(days=1)})
        self.assertFalse(form.is_valid())


# views testing

class ExpiredMedicinesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_meds =  7

        test_user = User.objects.create_user(username='testuser1', password='testpass1')
        test_user.save()

        for med_id in range(number_of_meds):
            Medicine.objects.create(
                trade_name=f'trade{med_id}',
                generic_name=f'generic{med_id}',
                unit_sell_price=10,
                unit_purchase_price=5,
                medicine_id = f'MED{med_id}'
            )
            Vendor.objects.create(
                vendor_name=f'vendor{med_id}',
                email=f'{med_id}@gmail.com',
                mobile=1234567890,
                address="testadd",
                vendor_id=f'VEN{med_id}',
                medicine_ids=f'MED{med_id}'
            )
            Stock.objects.create(
                medicine_id=f'MED{ med_id }',
                batch_id = f'BAT{ med_id }',
                quantity = 50,
                threshold = 45 + med_id,
                expiry_date = datetime.date.today() + datetime.timedelta(days=med_id)
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('expiredmeds'))
        self.assertRedirects(response, '/app/login/')
        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='testpass1')
        response = self.client.get('/app/expiredmeds/')
        self.assertEqula(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='testpass1')
        response = self.client.get(reverse('expiredmeds'))
        self.assertEqula(response.status_code, 200)
    
    def test_list_all_expired(self):
        login = self.client.login(username='testuser1', password='testpass1')
        response = self.client.get(reverse('expiredmeds'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('medicine_list' in response.context)
        self.assertTrue(len(response.context['medicine_list']) == 1)

class PurchaseMedicinesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_meds =  7

        test_user = User.objects.create_user(username='testuser1', password='testpass1')
        test_user.save()

        for med_id in range(number_of_meds):
            Medicine.objects.create(
                trade_name=f'trade{med_id}',
                generic_name=f'generic{med_id}',
                unit_sell_price=10,
                unit_purchase_price=5,
                medicine_id = f'MED{med_id}'
            )
            Vendor.objects.create(
                vendor_name=f'vendor{med_id}',
                email=f'{med_id}@gmail.com',
                mobile=1234567890,
                address="testadd",
                vendor_id=f'VEN{med_id}',
                medicine_ids=f'MED{med_id}'
            )
            Stock.objects.create(
                medicine_id=f'MED{ med_id }',
                batch_id = f'BAT{ med_id }',
                quantity = 50,
                threshold = 45 + med_id,
                expiry_date = datetime.date.today() + datetime.timedelta(days=med_id)
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('purchasemeds'))
        self.assertRedirects(response, '/app/login/')
        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='testpass1')
        response = self.client.get('/app/purchasemeds/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='testpass1')
        response = self.client.get(reverse('purchasemeds'))
        self.assertEqual(response.status_code, 200)
    
    def test_list_all_to_purchase(self):
        response = self.client.get(reverse('purchasemeds'))
        login = self.client.login(username='testuser1', password='testpass1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('medicine_list' in response.context)
        self.assertTrue(len(response.context['medicine_list']) == 6)

class RevenueandProfitViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_sales = 7

        test_user = User.objects.create_user(username='test_user', password='testpass')
        test_user.save()

        for i in range(number_of_sales):
            Medicine.objects.create(
                trade_name=f'trade{i}',
                generic_name=f'generic{i}',
                unit_sell_price=10,
                unit_purchase_price=5,
                medicine_id = f'MED{i}'
            )
            Sales.objects.create(
                medicine_id=f'MED{ i }',
                quantity= 2
            )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('revenueprofit'))
        self.assertRedirects(response, '/app/login/')
        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['is_admin'] = False
        response = self.client.get('/app/revenueprofit/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['is_admin'] = False
        response = self.client.get(reverse('revenueprofit'))
        self.assertEqual(response.status_code, 200)

    def test_revenue_and_profit(self):
        login = self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['is_admin'] = False
        startdate = datetime.date.today() - datetime.timedelta(days=4)
        enddate = datetime.date.today()
        response = self.client.get(reverse('revenueprofit')+'?startdate='+str(startdate)+'&enddate='+str(enddate))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('revenue' in response.context)
        self.assertTrue('profit' in response.context)
        self.assertEqual(response.context['revenue'], 100)
        self.assertEqula(response.context['profit'], 50)