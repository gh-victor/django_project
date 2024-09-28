from django.test import TestCase
from ..models import ExpenditureCategory, Expenditure, IncomeCategory, Income
from datetime import datetime as dt
from django.contrib.auth import get_user_model
User = get_user_model()


# ↓↓↓ --------------------　ExpenditureCategoryのModelsのテスト　-------------------- ↓↓↓

number1 = 1
name1 = 'name1'

date1 = dt(2024, 1, 1)
price1 = 100
description1 = 'description1'


class ExpenditureCategoryModelTests(TestCase):
    ''' ExpenditureCategoryのModelのテスト '''


    def test_create_instance(self):
        self.assertEqual(ExpenditureCategory.objects.all().count(), 0)

        expenditure_category1 = ExpenditureCategory.objects.create(number=number1, name=name1)

        self.assertEqual(ExpenditureCategory.objects.all().count(), 1)

        self.assertEqual(expenditure_category1.number, number1)
        self.assertEqual(expenditure_category1.name, name1)

# ↑↑↑ --------------------　ExpenditureCategoryのModelsのテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　ExpenditureのModelsのテスト　-------------------- ↓↓↓

class ExpenditureModelTests(TestCase):
    ''' ExpenditureのModelのテスト '''

    @classmethod
    def setUpTestData(cls):
        cls.expenditure_category1 = ExpenditureCategory.objects.create(number=number1, name=name1)


    def test_create_instance(self):
        self.assertEqual(Expenditure.objects.all().count(), 0)

        expenditure1 = Expenditure.objects.create(category=self.expenditure_category1, date=date1, price=price1, description=description1)

        self.assertEqual(Expenditure.objects.all().count(), 1)

        self.assertEqual(expenditure1.category, self.expenditure_category1)
        self.assertEqual(expenditure1.date, date1)
        self.assertEqual(expenditure1.price, price1)
        self.assertEqual(expenditure1.description, description1)

# ↑↑↑ --------------------　ExpenditureのModelsのテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeCategoryのModelsのテスト　-------------------- ↓↓↓

class IncomeCategoryModelTests(TestCase):
    ''' IncomeCategoryのModelのテスト '''


    def test_create_instance(self):
        self.assertEqual(IncomeCategory.objects.all().count(), 0)

        expenditure_category1 = IncomeCategory.objects.create(number=number1, name=name1)

        self.assertEqual(IncomeCategory.objects.all().count(), 1)

        self.assertEqual(expenditure_category1.number, number1)
        self.assertEqual(expenditure_category1.name, name1)

# ↑↑↑ --------------------　IncomeCategoryのModelsのテスト　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeのModelsのテスト　-------------------- ↓↓↓

class IncomeModelTests(TestCase):
    ''' IncomeのModelのテスト '''


    @classmethod
    def setUpTestData(cls):
        cls.income_category1 = IncomeCategory.objects.create(number=number1, name=name1)


    def test_create_instance(self):
        self.assertEqual(Income.objects.all().count(), 0)

        income1 = Income.objects.create(category=self.income_category1, date=date1, price=price1, description=description1)

        self.assertEqual(Income.objects.all().count(), 1)

        self.assertEqual(income1.category, self.income_category1)
        self.assertEqual(income1.date, date1)
        self.assertEqual(income1.price, price1)
        self.assertEqual(income1.description, description1)

# ↑↑↑ --------------------　IncomeのModelsのテスト　-------------------- ↑↑↑