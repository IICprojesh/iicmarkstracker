from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home,name='add_students'),
    path('insert_marks', views.insert_marks,name='insert_marks'),
    path('get_results', views.get_results,name='get_results'),
]
