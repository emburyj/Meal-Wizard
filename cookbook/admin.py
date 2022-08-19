from django.contrib import admin
from cookbook.models import *
# Register your models here.

# class CategoryInline(admin.StackedInline):
#     model = Category.posts.through

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ('name', 'ing_type')})]
    list_display = ('name', 'ing_type')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ('name', 'rec_type', 'source', 'author')})]
    list_display = ('name', 'rec_type', 'source', 'author')

@admin.register(Cookbook)
class CookbookAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ('rec', 'ing', 'qty')})]
    list_display = ('rec', 'ing', 'qty')

@admin.register(RecipeCollection)
class RecipeCollectionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ('author',)})]
    list_display = ('rcid', 'author', 'created_date')


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ('rec_col', 'rid')})]
    list_display = ('rec_col', 'rid')