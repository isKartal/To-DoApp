from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('create/', views.create, name="create"),
    path('delete/<int:Todos_id>/', views.delete, name="delete"),
    path('yes_finish/<int:Todos_id>/', views.yes_finish, name="yes_finish"),
    path('no_finish/<int:Todos_id>/', views.no_finish, name="no_finish"),
    path('update/<int:Todos_id>/', views.update, name='update'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('task/<int:Todos_id>/', views.task_detail, name='task_detail'),
]
