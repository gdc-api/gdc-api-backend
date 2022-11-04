from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ["date_joined"]
    fieldsets = (
        ("Credentials", {
            "fields": (
                "email",
                "password"
            ),
        }),
        ("Personal data",{
            "fields":( 
                "first_name",
                "last_name",   
                "bio",  
                "phone",
            )
        }),
)

admin.site.register(User, CustomUserAdmin)
