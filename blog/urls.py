from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<str:obj_type>/<str:pk>/', views.post_detail, name='post_detail'),
    path('character/<str:pk>/?<str:message>', views.post_detail, name='post_detail_mes'),
]