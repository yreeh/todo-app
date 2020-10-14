from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('', views.index_view, name="index"),
    path('home/', views.home, name="home"),

    path('home/add_todo', views.add_todo, name="add_todo"),
    path('home/delete_todo/<int:todo_id>', views.delete_todo, name="delete_todo"),
]
