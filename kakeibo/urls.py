from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [

    path('expenditure_category/', views.ExpenditureCategoryIndexView.as_view(), name='expenditure_category_index'), 
    path('expenditure_category/create/', views.ExpenditureCategoryCreateView.as_view(), name='expenditure_category_create'), 
    path('expenditure_category/<int:pk>/update/', views.ExpenditureCategoryUpdateView.as_view(), name='expenditure_category_update'), 
    path('expenditure_category/<int:pk>/delete/', views.ExpenditureCategoryDeleteView.as_view(), name='expenditure_category_delete'), 

    path('expenditure/', views.ExpenditureIndexView.as_view(), name='expenditure_index'), 
    path('expenditure/chart/', views.ExpenditureChartView.as_view(), name='expenditure_chart'), 
    path('expenditure/create/', views.ExpenditureCreateView.as_view(), name='expenditure_create'), 
    path('expenditure/<int:pk>/update/', views.ExpenditureUpdateView.as_view(), name='expenditure_update'), 
    path('expenditure/<int:pk>/delete/', views.ExpenditureDeleteView.as_view(), name='expenditure_delete'), 
    path('expenditure/import/', views.ExpenditureImportView.as_view(), name='expenditure_import'),

    path('income_category/', views.IncomeCategoryIndexView.as_view(), name='income_category_index'), 
    path('income_category/create/', views.IncomeCategoryCreateView.as_view(), name='income_category_create'), 
    path('income_category/<int:pk>/update/', views.IncomeCategoryUpdateView.as_view(), name='income_category_update'), 
    path('income_category/<int:pk>/delete/', views.IncomeCategoryDeleteView.as_view(), name='income_category_delete'), 

    path('income/', views.IncomeIndexView.as_view(), name='income_index'), 
    path('income/create/', views.IncomeCreateView.as_view(), name='income_create'), 
    path('income/<int:pk>/update/', views.IncomeUpdateView.as_view(), name='income_update'), 
    path('income/<int:pk>/delete/', views.IncomeDeleteView.as_view(), name='income_delete'), 
    path('income/import/', views.IncomeImportView.as_view(), name='income_import'),
    path('income/export/', views.IncomeExportView, name='income_export'),
]