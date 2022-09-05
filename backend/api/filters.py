from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    """ Фильтр для рецептов """
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug', label='Tags')
    is_favorited = filters.BooleanFilter(
        method='get_favorite', label='Favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shopping', label='Is in shopping list')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'tags', 'is_in_shopping_cart')

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorite_recipe__user=self.request.user)
        return Recipe.objects.all()

    def get_shopping(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
