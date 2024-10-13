from django.contrib import admin
from .models import ExpenditureCategory, Expenditure, IncomeCategory, Income
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ExpenditureCategoryResource(resources.ModelResource):
    class Meta:
        model = ExpenditureCategory


@admin.register(ExpenditureCategory)
class ExpenditureCategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    ordering = ['id']

    resource_class = ExpenditureCategoryResource


class ExpenditureResource(resources.ModelResource):
    class Meta:
        model = Expenditure


@admin.register(Expenditure)
class ExpenditureAdmin(ImportExportModelAdmin):
    Fields = ('id', 'category', 'date', 'price', 'description')
    list_display = ('id', 'category', 'date', 'price', 'description')
    list_filter = ('date',)
    ordering = ['id']
    list_editable = ('category', 'date', 'price', 'description')

    resource_class = ExpenditureResource


class IncomeCategoryResource(resources.ModelResource):
    class Meta:
        model = IncomeCategory


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    ordering = ['id']

    resource_class = IncomeCategoryResource


class IncomeResource(resources.ModelResource):
    class Meta:
        model = Income


@admin.register(Income)
class IncomeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'category', 'date', 'price', 'description')
    list_filter = ('date',)
    ordering = ['id']
    list_editable = ('category', 'date', 'price', 'description')

    resource_class = IncomeResource