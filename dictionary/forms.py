from django.forms import ModelForm
from directory.models import *
from django import forms


class StatusForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Название')
    class Meta:
        model = Status
        fields = ['name']

class TypeForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Название')
    class Meta:
        model = TypeOperation
        fields = ['name']

class CategoryForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Название')
    type_operation = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=TypeOperation.objects.all(),label='Тип операции')
    class Meta:
        model = Categories
        fields = ['name', 'type_operation']

class SubcategoryForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Название')
    parent = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Categories.objects.all(),label='Категория')
    class Meta:
        model = Subcategories
        fields = ['name', 'parent']