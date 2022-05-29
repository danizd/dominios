from django.urls import path
from . import views

urlpatterns = [
    path('tabla', views.post_list),
    path('', views.formulario),
]
