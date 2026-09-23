from django.urls import path

from . import views


app_name = "books"


urlpatterns = [
    path("",views.home,name="home"),
    path("books/", views.book_list, name="book_list"),
    path("categories/",views.category_list,name="category_list",),
    path("<slug:slug>/", views.book_detail, name="book_detail"),
    path("category/<slug:slug>/",views.category_books,name="category_books",),
]