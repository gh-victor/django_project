from django import forms
from .models import ExpenditureCategory, Expenditure, IncomeCategory, Income
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone


# ↓↓↓ --------------------　ExpenditureCategory_Form　-------------------- ↓↓↓

class ExpenditureCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenditureCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['class'] = 'form-control'
        super().__init__(*args, **kwargs)

# ↑↑↑ --------------------　ExpenditureCategory_Form　-------------------- ↑↑↑

# ↓↓↓ --------------------　Expenditure_Form　-------------------- ↓↓↓

class ExpenditureSearchForm(forms.Form):
    start_year = 2024
    end_year = timezone.now().year + 1
    years = [(year, f'{year}年') for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))
    YEAR_CHOICES = tuple(years)

    months = [(month, f'{month}月') for month in range(1, 13)]
    months.insert(0, (0, ''))
    MONTH_CHOICES = tuple(months)

    year = forms.ChoiceField(
        label='年',
        required=False,
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

    month = forms.ChoiceField(
        label='月',
        required=False,
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

    category = forms.ModelChoiceField(
        label='カテゴリ',
        required=False,
        queryset=ExpenditureCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form'})
    )

    key_word = forms.CharField(
        label='備考',
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': '空白区切りで複数のキーワード入力可'
        })
    )


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['class'] = 'form-control'
        super().__init__(*args, **kwargs)

# ↑↑↑ --------------------　Expenditure_Form　-------------------- ↑↑↑

# ↓↓↓ --------------------　IncomeCategory_Form　-------------------- ↓↓↓

class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['class'] = 'form-control'
        super().__init__(*args, **kwargs)

# ↑↑↑ --------------------　IncomeCategory_Form　-------------------- ↑↑↑

# ↓↓↓ --------------------　Income_Form　-------------------- ↓↓↓

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['class'] = 'form-control'
        super().__init__(*args, **kwargs)

# ↑↑↑ --------------------　Income_Form　-------------------- ↑↑↑

# ↓↓↓ --------------------　CSVUpload_Form　-------------------- ↓↓↓

class CsvUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル')

# ↑↑↑ --------------------　CSVUpload_Form　-------------------- ↑↑↑