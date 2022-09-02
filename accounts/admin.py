from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import IcoUser

class UserAdmin(UserAdmin):

    ordering = ('username', 'email',)
    list_display = ('username', 'email', 'is_admin',)
    search_fields = ('username', 'email','first_name')
    readonly_fields = ('date_joined', 'last_login',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None,{'fields': ('username', 'email', 'password')}),
        ('Personal Information',{'fields' : ('first_name', 'last_name', 'age', 'gender', 'phone_no')}),
        ('Permissions',{'fields': ('is_staff', 'is_admin', 'is_superuser', 'is_active')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

admin.site.register(IcoUser, UserAdmin)