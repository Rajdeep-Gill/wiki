from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('randomPage', views.randomPage, name='randomPage'),
    path("create", views.newPage, name="create"),
    path("search", views.search, name="search"),
    path("entry/<str:title>", views.entries, name="entries"),
    path("edit/<str:title>", views.edit, name="edit"),

]
