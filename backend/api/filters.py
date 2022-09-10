from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    """ Фильтр для рецептов """
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    # tags = filters.AllValuesMultipleFilter(
    #     field_name='tags__slug', label='Tags')
    is_favorited = filters.BooleanFilter(
        method='get_favorite', label='Favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shopping', label='Is in shopping list')

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'tags',
            'is_in_shopping_cart'
        )

    def get_favorite(self, queryset, name, value):

        user = self.request.user
        if value:
            return Recipe.objects.filter(
                favorite_recipe__user=user
            )
        return Recipe.objects.all().exclude(
            favorite_recipe__user=user
        )

    def get_shopping(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(
                shopping_cart__user=user
            )
        return Recipe.objects.all().exclude(
            favorite_recipe__user=user
        )


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
