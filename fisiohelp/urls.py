from django.urls import path, re_path
from . import views

app_name = 'fisiohelp'

urlpatterns = [
    path('', views.main, name='main'),
    path('<str:lang>', views.main, name='main'),
    path('<str:lang>/<slug:page>', views.main, name='main'),
]
