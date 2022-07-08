from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario),
    path('tabla', views.post_list),
    path('grafico', views.grafico),
    path('jaja', views.jaja),

]
