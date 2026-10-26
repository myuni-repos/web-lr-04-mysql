from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('files/', views.file_list, name='file_list'),
    path('database/', views.database_list, name='database_list'),
    path('database/search/', views.search_grades, name='search_grades'),
    path('database/<int:pk>/edit/', views.edit_grade, name='edit_grade'),
    path('database/<int:pk>/delete/', views.delete_grade, name='delete_grade'),
    path('upload/', views.upload_file, name='upload_file'),
]
