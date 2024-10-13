import io
import pandas as pd
import numpy as np
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import ExpenditureCategory, Expenditure, IncomeCategory, Income
from .forms import ExpenditureCategoryForm, ExpenditureSearchForm, ExpenditureForm, IncomeCategoryForm, IncomeForm
from .forms import CsvUploadForm
from . import function
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django_pandas.io import read_frame
from django.core import paginator
from django.contrib import messages
from urllib.parse import urlencode
from django.contrib.auth import get_user_model
User = get_user_model()


# ↓↓↓ --------------------　ExpenditureCategory　-------------------- ↓↓↓

class ExpenditureCategoryIndexView(LoginRequiredMixin, generic.ListView):
    model = ExpenditureCategory
    template_name = 'kakeibo/expenditure_category_index.html'


class ExpenditureCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ExpenditureCategoryForm
    template_name = 'kakeibo/expenditure_category_create.html'
    success_url = reverse_lazy('kakeibo:expenditure_category_index')


class ExpenditureCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ExpenditureCategory
    form_class = ExpenditureCategoryForm
    template_name = 'kakeibo/expenditure_category_update.html'
    success_url = reverse_lazy('kakeibo:expenditure_category_index')


class ExpenditureCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ExpenditureCategory
    template_name = 'kakeibo/expenditure_category_delete.html'
    success_url = reverse_lazy('kakeibo:expenditure_category_index')
    
# ↑↑↑ --------------------　ExpenditureCategory　-------------------- ↑↑↑

# ↓↓↓ --------------------　Expenditure　-------------------- ↓↓↓

def queryset_filter1(year, month, *, category=None, key_word=None):
    queryset = Expenditure.objects.all().order_by('date')

    if category:
        queryset = queryset.filter(category=category)

    if year and year != '0':
        queryset = queryset.filter(date__year=year)

    if month and month != '0':
        queryset = queryset.filter(date__month=month)

    if key_word:
        if key_word:
            for word in key_word.split():
                queryset = queryset.filter(description__icontains=word)

    return queryset

paginate_number = 10


class ExpenditureIndexView(LoginRequiredMixin, generic.FormView):
    template_name = 'kakeibo/expenditure_index.html'
    form_class = ExpenditureSearchForm
    success_url = reverse_lazy('kakeibo:expenditure_index')

    def form_valid(self, form):
        category = form.cleaned_data.get('category')
        year = form.cleaned_data.get('year')
        month = form.cleaned_data.get('month')
        key_word = form.cleaned_data.get('key_word')

        queryset = queryset_filter1(year, month, category=category, key_word=key_word)

        if 'search' in self.request.POST:
            if category:
                filter_word = urlencode({'category': category.pk, 'year': year, 'month': month, 'key_word': key_word})
            else:
                filter_word = urlencode({'year': year, 'month': month, 'key_word': key_word})

            return redirect(reverse('kakeibo:expenditure_index') + '?page=1&' + filter_word)
        
        elif 'export' in self.request.POST:
            response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
            response['Content-Disposition'] = 'filename="Expenditure.csv"'
            df = read_frame(queryset)
            df.to_csv(response, sep=',', index=False, encoding='utf-8')
            return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        key_word = self.request.GET.get('key_word')
        queryset = queryset_filter1(year, month, category=category, key_word=key_word)

        paginated_by = paginate_number
        my_paginator = paginator.Paginator(queryset, paginated_by)

        page = self.request.GET.get('page')
        try:
            page_obj = my_paginator.page(page)
        except (paginator.PageNotAnInteger, paginator.EmptyPage):
            page_obj = my_paginator.page(1)

        context['page_obj'] = page_obj
        context['expenditure_list'] = page_obj.object_list

        if '&' in self.request.GET.urlencode():
            filter_word = self.request.GET.urlencode()
            filter_word = filter_word[filter_word.index('&'):]
            context['filter_word'] = filter_word

        return context

        
class ExpenditureChartView(generic.ListView):
    model = Expenditure
    template_name = 'kakeibo/expenditure_chart.html'

    def get_queryset(self):
        queryset =  super().get_queryset()
        self.form = form = ExpenditureSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            queryset = queryset_filter1(year, month)

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.form = form = ExpenditureSearchForm(self.request.GET or None)
        context['form'] = self.form

        queryset = self.get_queryset()

        df = read_frame(queryset)

        total_expenditure_price = sum([row.price for row in df.itertuples()])
        context['total_expenditure_price'] = total_expenditure_price

        df['month'] = pd.to_datetime(df['date']).dt.strftime('%y-%m')
        df_chart1 = pd.pivot_table(df, index='month', values='price', aggfunc=np.sum)
        df_chart1 = df_chart1.sort_values('month')

        x = [row[0] for row in df_chart1.itertuples()]
        y = [row.price for row in df_chart1.itertuples()]
        chart1 = function.create_barchart(x, y)
        context['chart1'] = chart1


        df_chart2 = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)

        totals_for_each_category = [
            [row[0], row.price, f'{(row.price / total_expenditure_price)*100:.2f}%', ExpenditureCategory.objects.get(name=row[0]).number]
            for row in df_chart2.itertuples()]
        totals_for_each_category = sorted(totals_for_each_category, key=lambda x: x[3])

        category_list = [row[0] for row in totals_for_each_category]
        price_list = [row[1] for row in totals_for_each_category]
        chart2 = function.create_piechart(price_list, category_list)
        context['chart2'] = chart2
        
        context['totals_for_each_category'] = totals_for_each_category

        income_queryset = Income.objects.all().order_by('pk')
        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')

            if year and year != '0':
                income_queryset = income_queryset.filter(date__year=year)

            if month and month != '0':
                income_queryset = income_queryset.filter(date__month=month)

        df_income = read_frame(income_queryset)
        total_income_price = sum([row.price for row in df_income.itertuples()])
        context['total_income_price'] = total_income_price

        context['total_income_and_expenditure_price'] = total_income_price - total_expenditure_price

        return context


class ExpenditureCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ExpenditureForm
    template_name = 'kakeibo/expenditure_create.html'
    success_url = reverse_lazy('kakeibo:expenditure_index')
    

class ExpenditureUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Expenditure
    form_class = ExpenditureForm
    template_name = 'kakeibo/expenditure_update.html'
    success_url = reverse_lazy('kakeibo:expenditure_index')


class ExpenditureDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Expenditure
    template_name = 'kakeibo/expenditure_delete.html'
    success_url = reverse_lazy('kakeibo:expenditure_index')


class ExpenditureImportView(generic.FormView):
    template_name = 'kakeibo/expenditure_import.html'
    form_class = CsvUploadForm
    success_url = reverse_lazy('kakeibo:expenditure_index')

    def form_valid(self, form):
        cleaned_data_file = form.cleaned_data['file']
        df = pd.read_csv(io.TextIOWrapper(cleaned_data_file))

        saved_expenditure_object_exsist = None
        expenditure_objects_for_update = []
        expenditure_objects_for_create = []

        for row in df.itertuples():
            if len(Expenditure.objects.filter(pk=row.id).values()) >= 1:
                saved_expenditure_object_exsist = True
                expenditure = Expenditure.objects.get(pk=row.id)
            else:
                saved_expenditure_object_exsist = False
                expenditure = Expenditure(pk=row.id)
                
            expenditure.category = ExpenditureCategory.objects.get(name=row.category)
            expenditure.date = pd.to_datetime(row.date)
            expenditure.price = row.price
            expenditure.description = row.description
            
            if saved_expenditure_object_exsist:
                expenditure_objects_for_update.append(expenditure)
            else:
                expenditure_objects_for_create.append(expenditure)

        Expenditure.objects.bulk_update(expenditure_objects_for_update, fields=['category', 'date', 'price', 'description'])
        Expenditure.objects.bulk_create(expenditure_objects_for_create)

        return super().form_valid(form)

# ↑↑↑ --------------------　Expenditure　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeCategory　-------------------- ↓↓↓

class IncomeCategoryIndexView(LoginRequiredMixin, generic.ListView):
    model = IncomeCategory
    template_name = 'kakeibo/income_category_index.html'


class IncomeCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = IncomeCategoryForm
    template_name = 'kakeibo/income_category_create.html'
    success_url = reverse_lazy('kakeibo:income_category_index')


class IncomeCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = 'kakeibo/income_category_update.html'
    success_url = reverse_lazy('kakeibo:income_category_index')


class IncomeCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = IncomeCategory
    template_name = 'kakeibo/income_category_delete.html'
    success_url = reverse_lazy('kakeibo:income_category_index')
    
# ↑↑↑ --------------------　IncomeCategory　-------------------- ↑↑↑

# ↓↓↓ --------------------　Income　-------------------- ↓↓↓

class IncomeIndexView(LoginRequiredMixin, generic.ListView):
    model = Income
    template_name = 'kakeibo/income_index.html'
    ordering = ['date']
    paginated_by = 20


class IncomeCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = IncomeForm
    template_name = 'kakeibo/income_create.html'
    success_url = reverse_lazy('kakeibo:income_index')
   

class IncomeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'kakeibo/income_update.html'
    success_url = reverse_lazy('kakeibo:income_index')


class IncomeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Income
    template_name = 'kakeibo/income_delete.html'
    success_url = reverse_lazy('kakeibo:income_index')


class IncomeImportView(generic.FormView):
    template_name = 'kakeibo/income_import.html'
    form_class = CsvUploadForm
    success_url = reverse_lazy('kakeibo:income_index')

    def form_valid(self, form):
        cleaned_data_file = form.cleaned_data['file']
        df = pd.read_csv(io.TextIOWrapper(cleaned_data_file))

        saved_income_object_exsist = None
        income_objects_for_update = []
        income_objects_for_create = []

        for row in df.itertuples():
            if len(Income.objects.filter(pk=row.id).values()) >= 1:
                saved_income_object_exsist = True
                income = Income.objects.get(pk=row.id)
            else:
                saved_income_object_exsist = False
                income = Income(pk=row.id)
                
            income.category = IncomeCategory.objects.get(name=row.category)
            income.date = pd.to_datetime(row.date)
            income.price = row.price
            income.description = row.description

            if saved_income_object_exsist:
                income_objects_for_update.append(income)
            else:
                income_objects_for_create.append(income)

        Income.objects.bulk_update(income_objects_for_update, fields=['category', 'date', 'price', 'description'])
        Income.objects.bulk_create(income_objects_for_create)

        return super().form_valid(form)


def IncomeExportView(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = 'filename="Income.csv"'
    queryset = Income.objects.all()
    df = read_frame(queryset)
    df.to_csv(response, sep=',', index=False, encoding='utf-8')
    return response

# ↑↑↑ --------------------　Income　-------------------- ↑↑↑