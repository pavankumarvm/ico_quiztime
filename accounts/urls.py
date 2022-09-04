from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name="login_user"),
    path('adminlogin/', views.login_admin, name="login_admin"),
    path('logout/', views.logout_user, name="logout_user"),
    # path('forgot-password/', views.forgot_password, name="forgot-password"),
    # path('reset-password/', views.reset_password, name ="reset-password"),
    path('change_password/', views.change_password, name='change_password'),
    path('new_admin/', views.new_admin, name='register_user'),
    path('make_admin/', views.make_admin, name='make_admin'),
    path('change_status/', views.change_status, name='change_status'),
    path('update_details/', views.update_details, name='update_details'),
]