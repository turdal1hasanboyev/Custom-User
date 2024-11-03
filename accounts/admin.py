# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # `CustomUser` modelini import qiling


class CustomUserAdmin(UserAdmin):
    # Admin paneldagi ustunlarni ko'rsatish uchun
    list_display = ('id', 'email', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'gender')
    search_fields = ('email', 'phone_number')

    # `CustomUser` modelida username o'rniga email ishlatilayotganligi uchun, `UserAdmin`da `USERNAME_FIELD` o'zgartirish kerak.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'gender', 'adress', 'description')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Foydalanuvchi yaratishda majburiy maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    ordering = ('id',)
    filter_horizontal = ()

# Admin panelda CustomUserAdmin sinfini ro'yxatdan o'tkazish
admin.site.register(CustomUser, CustomUserAdmin)