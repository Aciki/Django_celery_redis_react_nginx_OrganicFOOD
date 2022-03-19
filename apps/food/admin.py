from django.contrib import admin

from .models import Food, FoodViews


class FoodAdmin(admin.ModelAdmin):
    list_display = ["title", "country"]
    

admin.site.register(Food, FoodAdmin)
admin.site.register(FoodViews)
