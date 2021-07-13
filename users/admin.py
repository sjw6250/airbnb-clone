from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    
    """Custom User Admin"""
    
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom profile",
            {
                "fields" : (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            }
        ),
    )

    # list_display = (
    #     "username",
    #     "first_name",
    #     "last_name",
    #     "email",
    #     "preference",
    #     "language",
    #     "fav_book_genre",
    #     "fav_movie_genre",
    # )

    # list_filter = (
    #     "preference",
    #     "language",
    #     "fav_book_genre",
    #     "fav_movie_genre",
    # )