from django.contrib import admin
from django.urls import path
from . import views

app_name="article"

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path("add/", views.add_article),
    path("view/<int:id>", views.viewArticle),
    path("edit/<int:id>", views.edit),
    path("delete/<int:id>", views.delete),
    path("", views.allArticles, name="articles"),
    path("comment/<int:id>", views.addComment),
]