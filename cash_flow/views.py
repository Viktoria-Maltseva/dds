from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from directory.models import *


# Представление для рендеринга главной страницы с таблицей.
# Метод обрабатыыает GET запросы.
@require_http_methods(['GET'])
def main_table(request):
    records = DDS.objects.all()

    # Все категории, подкатегории и статусы в словаре для выбора фильтрации.
    statuses = Status.objects.all()
    categories = Categories.objects.all()
    subcategories = Subcategories.objects.all()

    # Получение параметров фильтрации из GET-запроса.
    status = request.GET.get('status')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Фильтрация по заданным полям.
    if status:
        records = records.filter(status=status)
    if category:
        records = records.filter(category=category)
    if subcategory:
        records = records.filter(subcategory=subcategory)
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)

    # Рендеринг главной страницы.
    return render(request, 'homepage.html', 
        {'records': records,
        'statuses': statuses,
        'categories': categories,
        'subcategories': subcategories,
        'start_date': start_date,
        'end_date': end_date,})

# Представление для получения ID записи и действия с ним. Используется при выборе записи для редактирования.
@require_http_methods(['POST'])
def get_note_id(request):
    note_id = request.POST.get('note_id')
    action = request.POST.get('action')
    if note_id and action:
        request.session['note_id'] = note_id # Сохранение id записи в сессии.
        return redirect('note_update') # Перенаправление на страницу редактирования записи.
    return redirect('main_page')