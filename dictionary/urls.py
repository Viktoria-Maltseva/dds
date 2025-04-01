from django.urls import path
from dictionary.views import *


urlpatterns = [
    path('manage/', ManageDictionaryView.as_view(), name='manage_dictionary'),
    path('manage/edit/<str:item_type>/<int:item_id>/', EditItemView.as_view(), name='edit_item'),
    path('manage/delete/<str:item_type>/<int:item_id>/', DeleteView.as_view(), name='delete_item'),
]
