from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name="login_user"),
    path('adminlogin/', views.login_admin, name="login_admin"),
    path('logout/', views.logout_user, name="logout_user"),
    # path('forgot-password/', views.forgot_password, name="forgot-password"),
    # path('reset-password/', views.reset_password, name ="reset-password"),
    path('change_password/', views.change_password, name='change_password'),
    path('new_admin/', views.register_user, name='register_user'),
    path('new_user/', views.register_user, name='register_user'),
]