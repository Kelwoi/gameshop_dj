from django.contrib import admin
from .models import Category, Game

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "platform", "price_czk", "in_stock", "created_at")
    list_filter = ("category", "platform", "in_stock")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)
