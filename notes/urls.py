from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signupuser,name='signupuser'),
    path('login/', views.loginuser,name='loginuser'),
    path('logout/', views.logoutuser,name='logoutuser'),
    path('create/', views.createnote, name='createnote'),
    path('<int:notes_pk>/', views.viewnotes ,name='viewnotes'),
    path('<int:notes_pk>/delete', views.deletenote ,name='deletenote'),
]
