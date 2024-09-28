from django.db import models


class ExpenditureCategory(models.Model):
    number = models.IntegerField('カテゴリNo')
    name = models.CharField('カテゴリ名', max_length=20)

    def __str__(self):
        return self.name


class Expenditure(models.Model):
    category = models.ForeignKey(ExpenditureCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    description = models.TextField('備考', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    

class IncomeCategory(models.Model):
    number = models.IntegerField('カテゴリNo')
    name = models.CharField('カテゴリ名', max_length=20)

    def __str__(self):
        return self.name


class Income(models.Model):
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    description = models.TextField('備考', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')