from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from cash_flow import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_table, name='main_page'),
    path('set_note_id/', views.get_note_id, name='set_note_id'),
    path('note/', include('directory.urls')),
    path('dictionary/', include('dictionary.urls')),
]
