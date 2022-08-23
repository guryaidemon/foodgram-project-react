from django.contrib import admin

from foodgram import settings
from recipes.models import (
    Ingredient,
    IngredientsRecipe,
    Recipe,
    Tag,
    TagsRecipe
)


class IngredientsInline(admin.TabularInline):
    model = IngredientsRecipe
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagsRecipe
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_recipes_favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = settings.EMPTY
    inlines = [
        TagsInline,
        IngredientsInline
    ]
    readonly_fields = ['count_recipes_favorite']

    def count_recipes_favorite(self, obj):
        return obj.favorite_recipes.count()

    count_recipes_favorite.short_description = 'Популярность'


class TagsAdmin(admin.ModelAdmin):
    inlines = [
        TagsInline
    ]
    list_display = ('name', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInline
    ]
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
