"""ico_quiztime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from adminpanel.views import *

urlpatterns = [
  path('', index, name='index'),
  path('adminpanel/dashboard/', adminpanel, name='adminpanel'),
  path('adminpanel/profile/', adminprofile, name='profile'),
  path('adminpanel/create_quiz/', create_quiz, name='adminpanel'),
  path('adminpanel/edit_quiz/', edit_quiz, name='adminpanel'),
  path('adminpanel/delete_quiz/', delete_quiz, name='adminpanel'),
  path('adminpanel/newadmin', add_new_admin, name='add_new_admin'),
  # User APIS
  path('user/dashboard/', dashboard, name='dashboard'),
  path('user/profile/', profile, name='profile'),
  path('user/leaderboard/', leaderboard, name='leaderboard'),
  path('user/personal_scores/', personal_scores, name='personal_scores'),
  path('user/rules/',user_rules,name='user_rules'),
  path('user/take_quiz/', take_quiz, name='take_quiz'),
]
