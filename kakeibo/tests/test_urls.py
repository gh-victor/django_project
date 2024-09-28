from django.test import TestCase
from django.urls import resolve, reverse
from .. import views
from ..models import ExpenditureCategory, Expenditure, IncomeCategory, Income
from datetime import datetime as dt

# ↓↓↓ --------------------　ExpenditureCategoryのUrlsテスト　-------------------- ↓↓↓

class ExpenditureCategoryUrlsTests(TestCase):
  """ URLのテスト"""


  @classmethod
  def setUpTestData(cls):
      ExpenditureCategory.objects.create(number=1, name='name1')


  def test_expenditure_category_index_url(self):
    """ ExpenditureCategoryIndexViewのクラスを呼び出せているかテスト """

    url = reverse('kakeibo:expenditure_category_index')
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureCategoryIndexView)


  def test_expenditure_category_create_url(self):
    """ ExpenditureCategoryCreateViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:expenditure_category_create')
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureCategoryCreateView)


  def test_expenditure_category_update_url(self):
    """ ExpenditureCategoryUpdateViewのクラスを呼び出せているかテスト """
    
    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk
    
    url = reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk])
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureCategoryUpdateView)


  def test_expenditure_category_delete_url(self):
    """ ExpenditureCategoryDeleteViewのクラスを呼び出せているかテスト """
    
    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    url = reverse('kakeibo:expenditure_category_delete', args=[expenditure_category1_pk])
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureCategoryDeleteView)

# ↑↑↑ --------------------　ExpenditureCategoryのUrlsテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　ExpenditureのUrlsテスト　-------------------- ↓↓↓

class ExpenditureUrlsTests(TestCase):
  """ URLのテスト"""


  @classmethod
  def setUpTestData(cls):
        expenditure_category1 = ExpenditureCategory.objects.create(number=1, name='name1')
        expenditure1 = Expenditure.objects.create(category=expenditure_category1, date=dt(2024, 1, 1), price=100, description='description1')


  def test_expenditure_index_url(self):
    """ ExpenditureIndexViewのクラスを呼び出せているかテスト """

    url = reverse('kakeibo:expenditure_index')
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureIndexView)


  def test_expenditure_chart_url(self):
    """ ExpenditureChartViewのクラスを呼び出せているかテスト """

    url = reverse('kakeibo:expenditure_chart')
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureChartView)


  def test_expenditure_create_url(self):
    """ ExpenditureCreateViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:expenditure_create')
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureCreateView)


  def test_expenditure_update_url(self):
    """ ExpenditureUpdateViewのクラスを呼び出せているかテスト """
    
    expenditure1_pk = Expenditure.objects.all()[0].pk

    url = reverse('kakeibo:expenditure_update', args=[expenditure1_pk])
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureUpdateView)


  def test_expenditure_delete_url(self):
    """ ExpenditureDeleteViewのクラスを呼び出せているかテスト """
    
    expenditure1_pk = Expenditure.objects.all()[0].pk

    url = reverse('kakeibo:expenditure_delete', args=[expenditure1_pk])
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureDeleteView)


  def test_expenditure_import_url(self):
    """ ExpenditureImportViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:expenditure_import')
    self.assertEqual(resolve(url).func.view_class, views.ExpenditureImportView)

# ↑↑↑ --------------------　ExpenditureのUrlsテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeCategoryのUrlsテスト　-------------------- ↓↓↓

class IncomeCategoryUrlsTests(TestCase):
  """ URLのテスト"""


  @classmethod
  def setUpTestData(cls):
      IncomeCategory.objects.create(number=1, name='name1')


  def test_income_category_index_url(self):
    """ IncomeCategoryIndexViewのクラスを呼び出せているかテスト """

    url = reverse('kakeibo:income_category_index')
    self.assertEqual(resolve(url).func.view_class, views.IncomeCategoryIndexView)


  def test_income_category_create_url(self):
    """ IncomeCategoryCreateViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:income_category_create')
    self.assertEqual(resolve(url).func.view_class, views.IncomeCategoryCreateView)


  def test_income_category_update_url(self):
    """ IncomeCategoryUpdateViewのクラスを呼び出せているかテスト """
    
    income_category1_pk = IncomeCategory.objects.all()[0].pk
    
    url = reverse('kakeibo:income_category_update', args=[income_category1_pk])
    self.assertEqual(resolve(url).func.view_class, views.IncomeCategoryUpdateView)


  def test_income_category_delete_url(self):
    """ IncomeCategoryDeleteViewのクラスを呼び出せているかテスト """
    
    income_category1_pk = IncomeCategory.objects.all()[0].pk

    url = reverse('kakeibo:income_category_delete', args=[income_category1_pk])
    self.assertEqual(resolve(url).func.view_class, views.IncomeCategoryDeleteView)

# ↑↑↑ --------------------　IncomeCategoryのUrlsテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeのUrlsテスト　-------------------- ↓↓↓

class IncomeUrlsTests(TestCase):
  """ URLのテスト"""


  @classmethod
  def setUpTestData(cls):
        income_category1 = IncomeCategory.objects.create(number=1, name='name1')
        income1 = Income.objects.create(category=income_category1, date=dt(2024, 1, 1), price=100, description='description1')


  def test_income_index_url(self):
    """ IncomeIndexViewのクラスを呼び出せているかテスト """

    url = reverse('kakeibo:income_index')
    self.assertEqual(resolve(url).func.view_class, views.IncomeIndexView)


  def test_income_create_url(self):
    """ IncomeCreateViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:income_create')
    self.assertEqual(resolve(url).func.view_class, views.IncomeCreateView)


  def test_income_update_url(self):
    """ IncomeUpdateViewのクラスを呼び出せているかテスト """
    
    income1_pk = Income.objects.all()[0].pk

    url = reverse('kakeibo:income_update', args=[income1_pk])
    self.assertEqual(resolve(url).func.view_class, views.IncomeUpdateView)


  def test_income_delete_url(self):
    """ IncomeDeleteViewのクラスを呼び出せているかテスト """
    
    income1_pk = Income.objects.all()[0].pk

    url = reverse('kakeibo:income_delete', args=[income1_pk])
    self.assertEqual(resolve(url).func.view_class, views.IncomeDeleteView)


  def test_income_import_url(self):
    """ IncomeImportViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:income_import')
    self.assertEqual(resolve(url).func.view_class, views.IncomeImportView)


  def test_income_export_url(self):
    """ IncomeExportViewのクラスを呼び出せているかテスト """
    
    url = reverse('kakeibo:income_export')
    self.assertEqual(resolve(url).func, views.IncomeExportView)

# ↑↑↑ --------------------　IncomeのUrlsテスト　-------------------- ↑↑↑