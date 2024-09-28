from django.test import TestCase
from ..models import ExpenditureCategory, IncomeCategory
from ..forms import ExpenditureCategoryForm, ExpenditureForm, IncomeCategoryForm, IncomeForm
from datetime import datetime as dt

# ↓↓↓ --------------------　ExpenditureCategoryのFormsテスト　-------------------- ↓↓↓

class ExpenditureCategoryFormTests(TestCase):

    def test_validation_by_correct_data(self):
        ''' 正しいデータでバリデーションが成功するかをテスト '''

        form_data = {
            'number': 1, 'name': 'name1'
        }
        form = ExpenditureCategoryForm(form_data)
        self.assertTrue(form.is_valid())


    def test_number_field_validation_by_incorrect_data(self):
        ''' numberフィールドの間違ったデータでバリデーションが失敗するかをテスト '''

        form_data = {
            'number': 'a', 'name': 'name1'
        }
        form = ExpenditureCategoryForm(form_data)
        self.assertFalse(form.is_valid())


    def test_name_field_character_limit_validation(self):
        ''' nameフィールドの文字数制限のバリデーションをテスト '''

        form_data = {
            'number': 1, 'name': 'a' * 21
        }
        form = ExpenditureCategoryForm(form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'number': 1, 'name': 'a' * 20
        }
        form = ExpenditureCategoryForm(form_data)
        self.assertTrue(form.is_valid())

# ↑↑↑ --------------------　ExpenditureCategoryのFormsテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　ExpenditureのFormsテスト　-------------------- ↓↓↓

class ExpenditureFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.expenditure_category1 = ExpenditureCategory.objects.create(number=1, name='name1')
        cls.date1 = dt(2024, 1, 2, 13, 24, 35)


    def test_validation_by_correct_data(self):
        ''' 正しいデータでバリデーションが成功するかをテスト '''

        form_data = {
            'category': self.expenditure_category1, 'date': self.date1, 'price': 100, 'description': 'description1'
        }
        form = ExpenditureForm(form_data)
        self.assertTrue(form.is_valid())


    def test_price_field_validation_by_incorrect_data(self):
        ''' priceフィールドの間違ったデータでバリデーションが失敗するかをテスト '''

        form_data = {
            'category': self.expenditure_category1, 'date': self.date1, 'price': 'a', 'description': 'description1'
        }
        form = ExpenditureForm(form_data)
        self.assertFalse(form.is_valid())


    def test_description_field_character_limit_validation(self):
        ''' descriptionフィールドの文字数制限のバリデーションをテスト '''

        form_data = {
            'category': self.expenditure_category1, 'date': self.date1, 'price': 100, 'description': 'a' * 100
        }
        form = ExpenditureForm(form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'category': self.expenditure_category1, 'date': self.date1, 'price': 100, 'description': 'a' * 101
        }
        form = ExpenditureForm(form_data)
        self.assertFalse(form.is_valid())

# ↑↑↑ --------------------　ExpenditureのFormsテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeCategoryのFormsテスト　-------------------- ↓↓↓

class IncomeCategoryFormTests(TestCase):

    def test_validation_by_correct_data(self):
        ''' 正しいデータでバリデーションが成功するかをテスト '''

        form_data = {
            'number': 1, 'name': 'name1'
        }
        form = IncomeCategoryForm(form_data)
        self.assertTrue(form.is_valid())


    def test_number_field_validation_by_incorrect_data(self):
        ''' numberフィールドの間違ったデータでバリデーションが失敗するかをテスト '''

        form_data = {
            'number': 'a', 'name': 'name1'
        }
        form = IncomeCategoryForm(form_data)
        self.assertFalse(form.is_valid())


    def test_name_field_character_limit_validation(self):
        ''' nameフィールドの文字数制限のバリデーションをテスト '''

        form_data = {
            'number': 1, 'name': 'a' * 21
        }
        form = IncomeCategoryForm(form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'number': 1, 'name': 'a' * 20
        }
        form = IncomeCategoryForm(form_data)
        self.assertTrue(form.is_valid())

# ↑↑↑ --------------------　IncomeCategoryのFormsテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeのFormsテスト　-------------------- ↓↓↓

class IncomeFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.income_category1 = IncomeCategory.objects.create(number=1, name='name1')
        cls.date1 = dt(2024, 1, 2, 13, 24, 35)


    def test_validation_by_correct_data(self):
        ''' 正しいデータでバリデーションが成功するかをテスト '''

        form_data = {
            'category': self.income_category1, 'date': self.date1, 'price': 100, 'description': 'description1'
        }
        form = IncomeForm(form_data)
        self.assertTrue(form.is_valid())


    def test_price_field_validation_by_incorrect_data(self):
        ''' priceフィールドの間違ったデータでバリデーションが失敗するかをテスト '''

        form_data = {
            'category': self.income_category1, 'date': self.date1, 'price': 'a', 'description': 'description1'
        }
        form = IncomeForm(form_data)
        self.assertFalse(form.is_valid())


    def test_description_field_character_limit_validation(self):
        ''' descriptionフィールドの文字数制限のバリデーションをテスト '''

        form_data = {
            'category': self.income_category1, 'date': self.date1, 'price': 100, 'description': 'a' * 100
        }
        form = IncomeForm(form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'category': self.income_category1, 'date': self.date1, 'price': 100, 'description': 'a' * 101
        }
        form = IncomeForm(form_data)
        self.assertFalse(form.is_valid())

# ↑↑↑ --------------------　IncomeのFormsテスト　-------------------- ↑↑↑