from django.urls import path
from directory.views import *
from directory import views


urlpatterns = [
    path('create/', CreateNoteFormView.as_view(), name='note_create'),
    path('edit/', EditeNoteFormView.as_view(), name='note_update'),
    path('delete/<int:note_id>', DeleteNoteFormView.as_view(), name='note_delete'),
    path('ajax/load-categories/', views.load_categories, name='load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='load_subcategories'),
]
