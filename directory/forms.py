from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from datetime import datetime
from django import forms


# Форма для записи.
class NoteForm(ModelForm):
    # Поле для ввода даты. Инициализируется текущей датой в формате DD.MM.YYYY.
    date = forms.CharField(widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control'}), label='Дата',  initial=datetime.now().strftime('%d.%m.%Y'), required=False)
    summ = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Сумма', max_digits=10, decimal_places=2, required=True)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Комментарий', required=False)
    operation = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=TypeOperation.objects.all(), label='Тип операции', required=True)
    status = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Status.objects.all(), label='Статус', required=True)
    # Список категорий и подкатегорий инициализируется всеми позициями из словаря.
    # При выборе статуса список категорий обновляется в зависимости от выбранного статуса.
    # Список подкатегорий очищается, а заполняется после выбора категории.
    category = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Categories.objects.all(), label="Категория", required=True)
    subcategory = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Subcategories.objects.all(), label="Подкатегория", required=True)

    class Meta:
        model = DDS
        fields = ['date', 'status', 'operation', 'category', 'subcategory', 'summ', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Валидация поля date: проверка на соответсвующий формат DD.MM.YYYY
    # Если проверка не проходит, выбрасывается исключение ValidationError
    def clean_date(self):
        date_str = self.cleaned_data.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                return date_obj.date()
            except ValueError:
                raise ValidationError('Введите дату в формате: DD.MM.YYYY.')
        return None
    
    # Валидация данных формы:
    # Проверка суммы на обязательность и корректность (положительное число, максимальная длина = 10, максимальная длина целой части = 8).
    # Проверка типа операции, категории и подкатегории на соответствие условиям.
    # Категория должна соответствовать типу операции.
    # Подкатегория должна быть связана с выбранной категорией.
    def clean(self):
        cleaned_data = super().clean()
        summ = cleaned_data.get('summ')
        operation = cleaned_data.get('operation')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if not summ:
            self.add_error('summ', 'Сумма обязательна. Общее количество цифр в числе 10, в целой часть числа может быть не более 8 цифр.')
        elif summ <= 0:
            self.add_error('summ', 'Сумма должна быть положительным числом.')
        else:
            integer_part, decimal_part = str(summ).split('.') if '.' in str(summ) else str(summ), ''
            if len(integer_part) + len(decimal_part) > 10 or len(decimal_part) > 2:
                self.add_error('summ', 'Общее количество цифр в числе 10, в целой часть числа может быть не более 8 цифр.')

        if not operation:
            self.add_error('operation', 'Тип операции обязателен.')

        if not category:
            self.add_error('category', 'Категория обязательна.')

        if not subcategory:
            self.add_error('subcategory', 'Подкатегория обязательна.')
        
        if operation.id != category.type_operation.id:
            self.add_error('category', 'Категория не соответствует выбранному типу операции.')

        if category.id != subcategory.parent.id:
            self.add_error('subcategory', 'Подкатегория не соответствует выбранной категории.')

        return cleaned_data