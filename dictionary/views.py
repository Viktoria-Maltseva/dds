from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from directory.models import *


# Словари для хранения формы/модели каждого типа позиции в словаре.
# FORMS - соответствие типа позиции и формы.
# MODELS - соответствие типа позиции и модели базы данных.
# RU_DICT - отображение названий типов на русском языке.

FORMS = {
    'status': StatusForm,
    'type': TypeForm,
    'category': CategoryForm,
    'subcategory': SubcategoryForm
}

MODELS = {
    'status': Status,
    'type': TypeOperation,
    'category': Categories,
    'subcategory': Subcategories
}

RU_DICT = {
    'status': 'статус',
    'type': 'тип операции',
    'category': 'категорию',
    'subcategory': 'подкатегорию'
}


class ManageDictionaryView(View):
    # Метод для рендеринга главной страницы управления словарем.
    # Загружает формы для добавления элементов словаря и отображает все существующие элементы в словаре.
    def get(self, request, *args, **kwargs):
        # Получение форм для добавления новых элементов словаря.
        status_form = StatusForm()
        type_form = TypeForm()
        category_form = CategoryForm()
        subcategory_form = SubcategoryForm()

        # Получение всех позиций словаря.
        statuses = Status.objects.all()
        types = TypeOperation.objects.all()
        categories = Categories.objects.all()
        subcategories = Subcategories.objects.all()

        # Рендеринг главной страницы управления словарем.
        return render(request, 'dictionary/create_item.html', {
            'status_form': status_form,
            'type_form': type_form,
            'category_form': category_form,
            'subcategory_form': subcategory_form,
            'statuses': statuses,
            'types': types,
            'categories': categories,
            'subcategories': subcategories,
        })

    # Обработчик POST запроса для обработки отправленной формы.
    # Метод для добавления нового элемента в словарь.
    # На основе переданного типа позиции ('status', 'type', 'category', 'subcategory')
    # выбирается соответствующая форма и сохраняются данные.
    def post(self, request, *args, **kwargs):
        item = request.POST.get('item_type')
        form_class = FORMS.get(item) # Форма для заданного типа

        if not form_class:
            return redirect('manage_dictionary') # Если форма не найдена, перенаправляем на главную страницу управления словарем.

        form = form_class(request.POST) # Создание формы с переданными данными.
        if form.is_valid():
            form.save()
        return redirect('manage_dictionary') # Перенаправляем обратно на главную страницу управления словарем.

# Редактирование данных.
class EditItemView(View):
    def get(self, request, item_type, item_id, *args, **kwargs):
        model = MODELS.get(item_type) # Модель для заданного типа
        form_class = FORMS.get(item_type) # Форма для заданного типа

        instance = model.objects.get(id=item_id)
        try:
            instance = model.objects.get(id=item_id) # Редактируемый объект.
        except model.DoesNotExist:
            return redirect('manage_dictionary')

        form = form_class(instance=instance) # Заполнение формы данными для редактирования.
        return render(request, 'dictionary/edit_item.html', {
            'form': form,
            'item_type': RU_DICT.get(item_type),
            'item_id': item_id,
        })

    # Обработчик POST запроса для обработки отправленной формы.
    def post(self, request, item_type, item_id, *args, **kwargs):
        model = MODELS.get(item_type)
        form_class = FORMS.get(item_type)

        try:
            instance = model.objects.get(id=item_id) # Редактируемый объект.
        except model.DoesNotExist:
            return redirect('manage_dictionary')

        form = form_class(request.POST, instance=instance) # Форма с внесенными изменениями.
        if form.is_valid(): # Проверка данных.
            form.save() # Сохранение данных.
            return redirect('manage_dictionary') # Перенаправление на главную страницу управления словарем.

        return render(request, 'dictionary/edit_item.html', {
            'form': form,
            'item_type': RU_DICT.get(item_type),
            'item_id': item_id,
        })

# Удаление позиции словаря.
class DeleteView(View): 
    def post(self, request, *args, **kwargs):
        item_type = kwargs.get('item_type') # Получение типа позиции.
        item_id = kwargs.get('item_id') # id позиции.
        model = MODELS.get(item_type) # Модель позиции.
        item = model.objects.get(id=item_id) # Объект соответсующий позиции.
        if item:
            item.delete() # Удаление.
        return redirect('manage_dictionary') # Перенаправление на главную страницу управления словарем.
