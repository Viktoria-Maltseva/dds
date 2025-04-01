from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import NoteForm
from django.http import JsonResponse


class CreateNoteFormView(View):
    # Обработчик GET запроса для отображения формы создания новой записи.
    def get(self, request, *args, **kwargs):
        form = NoteForm() # Создается форма, инициализируется значениями по умолчанию.
        return render(request, 'create_note.html', {'form': form}) # Рендеринг страницы с формой.

    # Обработчик POST запроса для обработки отправленной формы.
    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST) # Создание формы с отправленными данными в POST запросе.
        if form.is_valid(): # Валидация формы.
            form.save() # Сохранение данных.
            return redirect('main_page') # Перенаправление на главную страницу.
        return render(request, 'create_note.html', {'form': form}) # Если форма не валидна, отображаем ее снова с введенными данными и ошибками.

class EditeNoteFormView(View):
    # Обработчик GET запроса для отображения формы создания новой записи.
    def get(self, request, *args, **kwargs):
        note_id = request.session['note_id'] # Получение id записи из сессии
        note = DDS.objects.get(id=note_id)
        form = NoteForm(instance=note) # Создание формы с данными существующей записи.
        return render(request, 'update_note.html', {'form': form}) # Рендеринг страницы с формой редактирования.

    # Обработчик POST запроса для обработки отправленных изменений.
    def post(self, request, *args, **kwargs):
        note_id = request.session['note_id'] # Получение id записи из сессии
        note = DDS.objects.get(id=note_id)
        form = NoteForm(request.POST, instance=note) # Создание формы с новыми данными, передаваемыми в POST-запросе.
        if form.is_valid(): # Валидация формы
            form.save()
            return redirect('main_page')
        return render(request, 'update_note.html', {'form': form})

class DeleteNoteFormView(View):
    # Обработчик POST запроса для удаления записи.
    def post(self, request, *args, **kwargs):
        note_id = kwargs.pop('note_id') # Получение ID записи из URL.
        note = DDS.objects.get(id=note_id)
        if note:
            note.delete() # Удаление.
        return redirect('main_page')

# Функция для загрузки категорий в зависимости от выбранного типа операции.
def load_categories(request):
    operation_id = request.GET.get('operation_id')
    categories = Categories.objects.filter(type_operation=operation_id)
    return JsonResponse(list(categories.values('id', 'name')), safe=False) # Отправка списока категорий в формате JSON.

# Функция для загрузки подкатегорий в зависимости от выбранной категории.
def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategories.objects.filter(parent_id=category_id)
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False) # Отправка списока подкатегорий в формате JSON.