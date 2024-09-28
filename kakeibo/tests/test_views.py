from django.test import TestCase
from django.urls import reverse
from ..models import ExpenditureCategory, Expenditure, IncomeCategory, Income
from ..forms import ExpenditureCategoryForm, ExpenditureForm, IncomeCategoryForm, IncomeForm
from datetime import datetime as dt
from django.contrib.auth import get_user_model
User = get_user_model()


# ↓↓↓ --------------------　ExpenditureCategoryのViewsのテスト　-------------------- ↓↓↓

# ExpenditureCategoryインスタンスを生成する為の変数
expenditure_category_number1 = 1
expenditure_category_name1 = 'name1'

expenditure_category_number2 = 2
expenditure_category_name2 = 'name2'

# ExpenditureCategoryインスタンスを生成する為のDict変数
expenditure_category_default_params1 ={
  'number': expenditure_category_number1,
  'name': expenditure_category_name1
}

expenditure_category_default_params2 ={
  'number': expenditure_category_number2,
  'name': expenditure_category_name2
}


def create_and_notsave_expenditure_category_by_default_params1():
  ''' デフォルト引数でExpenditureCategoryインスタンスを生成1 '''

  return ExpenditureCategory(number=expenditure_category_number1, name=expenditure_category_name1)


def create_and_notsave_expenditure_category_by_default_params2():
  ''' デフォルト引数でExpenditureCategoryインスタンスを生成2 '''

  return ExpenditureCategory(number=expenditure_category_number2, name=expenditure_category_name2)


def create_and_notsave_expenditure_category_by_input_argument(number, name):
  ''' 入力された引数でExpenditureCategoryインスタンスを生成 '''

  return ExpenditureCategory(number=number, name=name)

# 　　　↓↓↓ --------------------　ExpenditureCategoryIndexViewのテスト　-------------------- ↓↓↓

class ExpenditureCategoryIndexViewTests(TestCase):
  ''' ExpenditureCategoryIndexViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/expenditure_category/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure_category/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:expenditure_category_index'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure_category/')

  
  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_category_index'))
    self.assertEqual(response.status_code, 200)


  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_category_index'))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_category_index.html')


  def test_create_instance_and_reflect_to_template(self):
    ''' 作成したインスタンスのテンプレートへの反映をテスト(ログイン中) '''

    self.client.force_login(self.user)

    self.assertEqual(ExpenditureCategory.objects.all().count(), 0)

    expenditure_category1 = create_and_notsave_expenditure_category_by_default_params1()
    expenditure_category1.save()

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    response = self.client.get(reverse('kakeibo:expenditure_category_index'))
    self.assertQuerySetEqual(response.context['expenditurecategory_list'], [expenditure_category1])
    self.assertContains(response, expenditure_category1.number)
    self.assertContains(response, expenditure_category1.name)

# 　　　↑↑↑ --------------------　ExpenditureCategoryIndexViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　ExpenditureCategoryCreateViewのテスト　-------------------- ↓↓↓

class ExpenditureCategoryCreateViewTests(TestCase):
  ''' ExpenditureCategoryCreateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/expenditure_category/create/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure_category/create/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:expenditure_category_create'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure_category/create/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_category_create'))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_category_create'))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_category_create.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_category_create'))
    self.assertIsInstance(response.context['form'], ExpenditureCategoryForm)


  def test_create_and_save_by_valid_data(self):
    """ 正しいデータでPOSTして、ExpenditureCategoryインスタンスが生成されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(ExpenditureCategory.objects.all().count(), 0)

    self.client.post(
      reverse('kakeibo:expenditure_category_create'),
      expenditure_category_default_params1
    )

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)
    expenditure_category1 = ExpenditureCategory.objects.all()[0]
    self.assertEqual(expenditure_category1.number, expenditure_category_default_params1['number'])
    self.assertEqual(expenditure_category1.name, expenditure_category_default_params1['name'])


  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(ExpenditureCategory.objects.all().count(), 0)

    response = self.client.post(
      reverse('kakeibo:expenditure_category_create'),
      expenditure_category_default_params1
    )

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    self.assertRedirects(response, reverse('kakeibo:expenditure_category_index'))

# 　　　↑↑↑ --------------------　ExpenditureCategoryCreateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　ExpenditureCategoryUpdateViewのテスト　-------------------- ↓↓↓

class ExpenditureCategoryUpdateViewTests(TestCase):
  ''' ExpenditureCategoryUpdateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # ExpenditureCategoryインスタンスを生成
      expenditure_category1 = create_and_notsave_expenditure_category_by_default_params1()
      expenditure_category1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/expenditure_category/{expenditure_category1_pk}/update/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure_category/{expenditure_category1_pk}/update/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure_category/{expenditure_category1_pk}/update/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_category_update.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk]))
    self.assertIsInstance(response.context['form'], ExpenditureCategoryForm)


  def test_update_and_save_by_valid_data(self):
    """ 正しいデータでPOSTして、ExpenditureCategoryインスタンスが変更されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    expenditure_category1 = ExpenditureCategory.objects.all()[0]
    self.assertEqual(expenditure_category1.number, expenditure_category_default_params1['number'])
    self.assertEqual(expenditure_category1.name, expenditure_category_default_params1['name'])

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    self.client.post(
      reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk]),
      expenditure_category_default_params2
    )

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    expenditure_category2 = ExpenditureCategory.objects.get(pk=expenditure_category1_pk)
    self.assertEqual(expenditure_category2.number, expenditure_category_default_params2['number'])
    self.assertEqual(expenditure_category2.name, expenditure_category_default_params2['name'])


  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.post(
      reverse('kakeibo:expenditure_category_update', args=[expenditure_category1_pk]),
      expenditure_category_default_params2
    )

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    self.assertRedirects(response, reverse('kakeibo:expenditure_category_index'))

# 　　　↑↑↑ --------------------　ExpenditureCategoryUpdateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　ExpenditureCategoryDeleteViewのテスト　-------------------- ↓↓↓

class ExpenditureCategoryDeleteViewTests(TestCase):
  ''' ExpenditureCategoryDeleteViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # ExpenditureCategoryインスタンスを生成
      expenditure_category1 = create_and_notsave_expenditure_category_by_default_params1()
      expenditure_category1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/expenditure_category/{expenditure_category1_pk}/delete/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure_category/{expenditure_category1_pk}/delete/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_category_delete', args=[expenditure_category1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure_category/{expenditure_category1_pk}/delete/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_category_delete', args=[expenditure_category1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_category_delete', args=[expenditure_category1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_category_delete.html')


  def test_delete(self):
    """ 正しいデータでPOSTして、ExpenditureCategoryインスタンスが削除されることをテスト(ログイン中) """

    self.client.force_login(self.user)
    
    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    expenditure_category1_pk = ExpenditureCategory.objects.all()[0].pk

    self.client.post(
      reverse('kakeibo:expenditure_category_delete', args=[expenditure_category1_pk])
    )

    self.assertEqual(ExpenditureCategory.objects.all().count(), 0)



  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

    expenditure_category_pk = ExpenditureCategory.objects.all()[0].pk

    response = self.client.post(
      reverse('kakeibo:expenditure_category_delete', args=[expenditure_category_pk])
    )

    self.assertEqual(ExpenditureCategory.objects.all().count(), 0)

    self.assertRedirects(response, reverse('kakeibo:expenditure_category_index'))

# 　　　↑↑↑ --------------------　ExpenditureCategoryDeleteViewのテスト　-------------------- ↑↑↑

# ↑↑↑ --------------------　ExpenditureCategoryのViewsのテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　ExpenditureのViewsのテスト　-------------------- ↓↓↓

# Expenditureインスタンスを生成する為の変数
expenditure_date1 = dt(2024, 1, 1)
expenditure_price1 = 100
expenditure_description1 = 'description1'


def create_and_notsave_expenditure_by_default_params1(expenditure_category1):
  ''' デフォルト引数でExpenditureインスタンスを生成1 '''

  return Expenditure(
    category=expenditure_category1,
    date=expenditure_date1,
    price=expenditure_price1,
    description=expenditure_description1
  )


# 　　　↓↓↓ --------------------　ExpenditureIndexViewのテスト　-------------------- ↓↓↓

class ExpenditureIndexViewTests(TestCase):
  ''' ExpenditureIndexViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)

      cls.expenditure_category1 = ExpenditureCategory.objects.create(number=1, name='name1')
      cls.expenditure_category2 = ExpenditureCategory.objects.create(number=2, name='name2')


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/expenditure/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:expenditure_index'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure/')

  
  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_index'))
    self.assertEqual(response.status_code, 200)


  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_index'))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_index.html')


  def test_create_instance_and_reflect_to_template(self):
    ''' 作成したインスタンスのテンプレートへの反映をテスト(ログイン中) '''

    self.client.force_login(self.user)

    self.assertEqual(Expenditure.objects.all().count(), 0)

    expenditure1 = create_and_notsave_expenditure_by_default_params1(self.expenditure_category1)
    expenditure1.save()

    self.assertEqual(Expenditure.objects.all().count(), 1)

    response = self.client.get(reverse('kakeibo:expenditure_index'))
    self.assertQuerySetEqual(response.context['expenditure_list'], [expenditure1])
    self.assertContains(response, expenditure1.category)
    self.assertContains(response, f'{str(expenditure1.date.year)}年{str(expenditure1.date.month)}月{str(expenditure1.date.day)}日')
    self.assertContains(response, expenditure1.price)
    self.assertContains(response, expenditure1.description)

# 　　　↑↑↑ --------------------　ExpenditureIndexViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　ExpenditureCreateViewのテスト　-------------------- ↓↓↓

class ExpenditureCreateViewTests(TestCase):
  ''' ExpenditureCreateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/expenditure/create/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure/create/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:expenditure_create'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/expenditure/create/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_create'))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_create'))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_create.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:expenditure_create'))
    self.assertIsInstance(response.context['form'], ExpenditureForm)

# 　　　↑↑↑ --------------------　ExpenditureCreateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　ExpenditureUpdateViewのテスト　-------------------- ↓↓↓

class ExpenditureUpdateViewTests(TestCase):
  ''' ExpenditureUpdateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # ExpenditureCategoryインスタンスを生成
      cls.expenditure_category1 = ExpenditureCategory.objects.create(number=1, name='name1')

      # Expenditureインスタンスを生成
      expenditure1 = create_and_notsave_expenditure_by_default_params1(cls.expenditure_category1)
      expenditure1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/expenditure/{expenditure1_pk}/update/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure/{expenditure1_pk}/update/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_update', args=[expenditure1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure/{expenditure1_pk}/update/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure1_pk = Expenditure.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:expenditure_update', args=[expenditure1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure1_pk = Expenditure.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:expenditure_update', args=[expenditure1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_update.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_update', args=[expenditure1_pk]))
    self.assertIsInstance(response.context['form'], ExpenditureForm)

# 　　　↑↑↑ --------------------　ExpenditureUpdateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　ExpenditureDeleteViewのテスト　-------------------- ↓↓↓

class ExpenditureDeleteViewTests(TestCase):
  ''' ExpenditureDeleteViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # ExpenditureCategoryインスタンスを生成
      cls.expenditure_category1 = ExpenditureCategory.objects.create(number=1, name='name1')

      # Expenditureインスタンスを生成
      expenditure1 = create_and_notsave_expenditure_by_default_params1(cls.expenditure_category1)
      expenditure1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/expenditure/{expenditure1_pk}/delete/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure/{expenditure1_pk}/delete/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_delete', args=[expenditure1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/expenditure/{expenditure1_pk}/delete/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_delete', args=[expenditure1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    expenditure1_pk = Expenditure.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:expenditure_delete', args=[expenditure1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/expenditure_delete.html')


  def test_delete(self):
    """ 正しいデータでPOSTして、Expenditureインスタンスが削除されることをテスト(ログイン中) """

    self.client.force_login(self.user)
    
    self.assertEqual(Expenditure.objects.all().count(), 1)

    expenditure1_pk = Expenditure.objects.all()[0].pk

    self.client.post(
      reverse('kakeibo:expenditure_delete', args=[expenditure1_pk])
    )

    self.assertEqual(Expenditure.objects.all().count(), 0)


  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(Expenditure.objects.all().count(), 1)

    expenditure_pk = Expenditure.objects.all()[0].pk

    response = self.client.post(
      reverse('kakeibo:expenditure_delete', args=[expenditure_pk])
    )

    self.assertEqual(Expenditure.objects.all().count(), 0)

    self.assertRedirects(response, reverse('kakeibo:expenditure_index'))

# 　　　↑↑↑ --------------------　ExpenditureDeleteViewのテスト　-------------------- ↑↑↑

# ↑↑↑ --------------------　ExpenditureのViewsのテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeCategoryのViewsのテスト　-------------------- ↓↓↓

# IncomeCategoryインスタンスを生成する為の変数
income_category_number1 = 1
income_category_name1 = 'name1'

income_category_number2 = 2
income_category_name2 = 'name2'

# IncomeCategoryインスタンスを生成する為のDict変数
income_category_default_params1 ={
  'number': income_category_number1,
  'name': income_category_name1
}

income_category_default_params2 ={
  'number': income_category_number2,
  'name': income_category_name2
}


def create_and_notsave_income_category_by_default_params1():
  ''' デフォルト引数でIncomeCategoryインスタンスを生成1 '''

  return IncomeCategory(number=income_category_number1, name=income_category_name1)


def create_and_notsave_income_category_by_default_params2():
  ''' デフォルト引数でIncomeCategoryインスタンスを生成2 '''

  return IncomeCategory(number=income_category_number2, name=income_category_name2)


def create_and_notsave_income_category_by_input_argument(number, name):
  ''' 入力された引数でIncomeCategoryインスタンスを生成 '''

  return IncomeCategory(number=number, name=name)

# 　　　↓↓↓ --------------------　IncomeCategoryIndexViewのテスト　-------------------- ↓↓↓

class IncomeCategoryIndexViewTests(TestCase):
  ''' IncomeCategoryIndexViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/income_category/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income_category/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:income_category_index'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income_category/')

  
  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_category_index'))
    self.assertEqual(response.status_code, 200)


  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_category_index'))
    self.assertTemplateUsed(response, 'kakeibo/income_category_index.html')


  def test_create_instance_and_reflect_to_template(self):
    ''' 作成したインスタンスのテンプレートへの反映をテスト(ログイン中) '''

    self.client.force_login(self.user)

    self.assertEqual(IncomeCategory.objects.all().count(), 0)

    income_category1 = create_and_notsave_income_category_by_default_params1()
    income_category1.save()

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    response = self.client.get(reverse('kakeibo:income_category_index'))
    self.assertQuerySetEqual(response.context['incomecategory_list'], [income_category1])
    self.assertContains(response, income_category1.number)
    self.assertContains(response, income_category1.name)

# 　　　↑↑↑ --------------------　IncomeCategoryIndexViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　IncomeCategoryCreateViewのテスト　-------------------- ↓↓↓

class IncomeCategoryCreateViewTests(TestCase):
  ''' IncomeCategoryCreateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/income_category/create/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income_category/create/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:income_category_create'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income_category/create/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_category_create'))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_category_create'))
    self.assertTemplateUsed(response, 'kakeibo/income_category_create.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_category_create'))
    self.assertIsInstance(response.context['form'], IncomeCategoryForm)


  def test_create_and_save_by_valid_data(self):
    """ 正しいデータでPOSTして、IncomeCategoryインスタンスが生成されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(IncomeCategory.objects.all().count(), 0)

    self.client.post(
      reverse('kakeibo:income_category_create'),
      income_category_default_params1
    )

    self.assertEqual(IncomeCategory.objects.all().count(), 1)
    
    income_category1 = IncomeCategory.objects.all()[0]
    self.assertEqual(income_category1.number, income_category_default_params1['number'])
    self.assertEqual(income_category1.name, income_category_default_params1['name'])


  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(IncomeCategory.objects.all().count(), 0)

    response = self.client.post(
      reverse('kakeibo:income_category_create'),
      income_category_default_params1
    )

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    self.assertRedirects(response, reverse('kakeibo:income_category_index'))

# 　　　↑↑↑ --------------------　IncomeCategoryCreateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　IncomeCategoryUpdateViewのテスト　-------------------- ↓↓↓

class IncomeCategoryUpdateViewTests(TestCase):
  ''' IncomeCategoryUpdateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # IncomeCategoryインスタンスを生成
      income_category1 = create_and_notsave_income_category_by_default_params1()
      income_category1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/income_category/{income_category1_pk}/update/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income_category/{income_category1_pk}/update/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_category_update', args=[income_category1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income_category/{income_category1_pk}/update/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    income_category1_pk = IncomeCategory.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:income_category_update', args=[income_category1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_category_update', args=[income_category1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/income_category_update.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_category_update', args=[income_category1_pk]))
    self.assertIsInstance(response.context['form'], IncomeCategoryForm)


  def test_update_and_save_by_valid_data(self):
    """ 正しいデータでPOSTして、IncomeCategoryインスタンスが変更されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    income_category1 = IncomeCategory.objects.all()[0]
    self.assertEqual(income_category1.number, income_category_default_params1['number'])
    self.assertEqual(income_category1.name, income_category_default_params1['name'])

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    self.client.post(
      reverse('kakeibo:income_category_update', args=[income_category1_pk]),
      income_category_default_params2
    )

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    income_category2 = IncomeCategory.objects.get(pk=income_category1_pk)
    self.assertEqual(income_category2.number, income_category_default_params2['number'])
    self.assertEqual(income_category2.name, income_category_default_params2['name'])


  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.post(
      reverse('kakeibo:income_category_update', args=[income_category1_pk]),
      income_category_default_params2
    )

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    self.assertRedirects(response, reverse('kakeibo:income_category_index'))

# 　　　↑↑↑ --------------------　IncomeCategoryUpdateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　IncomeCategoryDeleteViewのテスト　-------------------- ↓↓↓

class IncomeCategoryDeleteViewTests(TestCase):
  ''' IncomeCategoryDeleteViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # IncomeCategoryインスタンスを生成
      income_category1 = create_and_notsave_income_category_by_default_params1()
      income_category1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/income_category/{income_category1_pk}/delete/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income_category/{income_category1_pk}/delete/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_category_delete', args=[income_category1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income_category/{income_category1_pk}/delete/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_category_delete', args=[income_category1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_category_delete', args=[income_category1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/income_category_delete.html')


  def test_delete(self):
    """ 正しいデータでPOSTして、IncomeCategoryインスタンスが削除されることをテスト(ログイン中) """

    self.client.force_login(self.user)
    
    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    income_category1_pk = IncomeCategory.objects.all()[0].pk

    self.client.post(
      reverse('kakeibo:income_category_delete', args=[income_category1_pk])
    )

    self.assertEqual(IncomeCategory.objects.all().count(), 0)



  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(IncomeCategory.objects.all().count(), 1)

    income_category_pk = IncomeCategory.objects.all()[0].pk

    response = self.client.post(
      reverse('kakeibo:income_category_delete', args=[income_category_pk])
    )

    self.assertEqual(IncomeCategory.objects.all().count(), 0)

    self.assertRedirects(response, reverse('kakeibo:income_category_index'))

# 　　　↑↑↑ --------------------　IncomeCategoryDeleteViewのテスト　-------------------- ↑↑↑

# ↑↑↑ --------------------　IncomeCategoryのViewsのテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeのViewsのテスト　-------------------- ↓↓↓

# Incomeインスタンスを生成する為の変数
income_date1 = dt(2024, 1, 1)
income_price1 = 100
income_description1 = 'description1'


def create_and_notsave_income_by_default_params1(income_category1):
  ''' デフォルト引数でIncomeインスタンスを生成1 '''

  return Income(
    category=income_category1,
    date=income_date1,
    price=income_price1,
    description=income_description1
  )


# 　　　↓↓↓ --------------------　IncomeIndexViewのテスト　-------------------- ↓↓↓

class IncomeIndexViewTests(TestCase):
  ''' IncomeIndexViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)

      cls.income_category1 = IncomeCategory.objects.create(number=1, name='name1')
      cls.income_category2 = IncomeCategory.objects.create(number=2, name='name2')


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/income/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:income_index'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income/')

  
  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_index'))
    self.assertEqual(response.status_code, 200)


  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_index'))
    self.assertTemplateUsed(response, 'kakeibo/income_index.html')


  def test_create_instance_and_reflect_to_template(self):
    ''' 作成したインスタンスのテンプレートへの反映をテスト(ログイン中) '''

    self.client.force_login(self.user)

    self.assertEqual(Income.objects.all().count(), 0)

    income1 = create_and_notsave_income_by_default_params1(self.income_category1)
    income1.save()

    self.assertEqual(Income.objects.all().count(), 1)

    response = self.client.get(reverse('kakeibo:income_index'))
    self.assertQuerySetEqual(response.context['income_list'], [income1])
    self.assertContains(response, income1.category)
    self.assertContains(response, f'{str(income1.date.year)}年{str(income1.date.month)}月{str(income1.date.day)}日')
    self.assertContains(response, income1.price)
    self.assertContains(response, income1.description)

# 　　　↑↑↑ --------------------　IncomeIndexViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　IncomeCreateViewのテスト　-------------------- ↓↓↓

class IncomeCreateViewTests(TestCase):
  ''' IncomeCreateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get('/kakeibo/income/create/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income/create/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    response = self.client.get(reverse('kakeibo:income_create'))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/accounts/login/?next=/kakeibo/income/create/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_create'))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_create'))
    self.assertTemplateUsed(response, 'kakeibo/income_create.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    response = self.client.get(reverse('kakeibo:income_create'))
    self.assertIsInstance(response.context['form'], IncomeForm)

# 　　　↑↑↑ --------------------　IncomeCreateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　IncomeUpdateViewのテスト　-------------------- ↓↓↓

class IncomeUpdateViewTests(TestCase):
  ''' IncomeUpdateViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # IncomeCategoryインスタンスを生成
      cls.income_category1 = IncomeCategory.objects.create(number=1, name='name1')

      # Incomeインスタンスを生成
      income1 = create_and_notsave_income_by_default_params1(cls.income_category1)
      income1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/income/{income1_pk}/update/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income/{income1_pk}/update/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_update', args=[income1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income/{income1_pk}/update/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    income1_pk = Income.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:income_update', args=[income1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    income1_pk = Income.objects.all()[0].pk
    
    response = self.client.get(reverse('kakeibo:income_update', args=[income1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/income_update.html')


  def test_use_correct_form(self):
    """ フォームが適切に表示されることをテスト(ログイン中) """

    self.client.force_login(self.user)

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_update', args=[income1_pk]))
    self.assertIsInstance(response.context['form'], IncomeForm)

# 　　　↑↑↑ --------------------　IncomeUpdateViewのテスト　-------------------- ↑↑↑

# 　　　↓↓↓ --------------------　IncomeDeleteViewのテスト　-------------------- ↓↓↓

class IncomeDeleteViewTests(TestCase):
  ''' IncomeDeleteViewをテスト '''


  @classmethod
  def setUpTestData(cls):

      # カスタムユーザーを生成
      cls.email="testuser@sample.com"
      cls.password="a12b34c5"
      cls.user = User.objects.create(email=cls.email, password=cls.password)
      
      # IncomeCategoryインスタンスを生成
      cls.income_category1 = IncomeCategory.objects.create(number=1, name='name1')

      # Incomeインスタンスを生成
      income1 = create_and_notsave_income_by_default_params1(cls.income_category1)
      income1.save()


  def test_get_by_url_strings_at_logout(self):
    ''' URLでの呼び出しをテスト(ログアウト中) '''

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(f'/kakeibo/income/{income1_pk}/delete/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income/{income1_pk}/delete/')


  def test_get_by_name_at_logout(self):
    ''' nameでの呼び出しをテスト(ログアウト中) '''

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_delete', args=[income1_pk]))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f'/accounts/login/?next=/kakeibo/income/{income1_pk}/delete/')


  def test_get_by_name_at_login(self):
    ''' nameでの呼び出しをテスト(ログイン中) '''

    self.client.force_login(self.user)

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_delete', args=[income1_pk]))
    self.assertEqual(response.status_code, 200)
  

  def test_use_correct_template(self):
    ''' 使用するテンプレートを調べるテスト(ログイン中) '''

    self.client.force_login(self.user)

    income1_pk = Income.objects.all()[0].pk

    response = self.client.get(reverse('kakeibo:income_delete', args=[income1_pk]))
    self.assertTemplateUsed(response, 'kakeibo/income_delete.html')


  def test_delete(self):
    """ 正しいデータでPOSTして、Incomeインスタンスが削除されることをテスト(ログイン中) """

    self.client.force_login(self.user)
    
    self.assertEqual(Income.objects.all().count(), 1)

    income1_pk = Income.objects.all()[0].pk

    self.client.post(
      reverse('kakeibo:income_delete', args=[income1_pk])
    )

    self.assertEqual(Income.objects.all().count(), 0)


  def test_redirects_after_post(self):
    """ 正しいデータでPOSTして、適切なページにリダイレクトすることをテスト(ログイン中) """

    self.client.force_login(self.user)

    self.assertEqual(Income.objects.all().count(), 1)

    income_pk = Income.objects.all()[0].pk

    response = self.client.post(
      reverse('kakeibo:income_delete', args=[income_pk])
    )

    self.assertEqual(Income.objects.all().count(), 0)

    self.assertRedirects(response, reverse('kakeibo:income_index'))

# 　　　↑↑↑ --------------------　IncomeDeleteViewのテスト　-------------------- ↑↑↑

# ↑↑↑ --------------------　IncomeのViewsのテスト　-------------------- ↑↑↑