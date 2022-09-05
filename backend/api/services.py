import csv

from django.db.models import Sum
from django.http import HttpResponse
from requests import Response
from rest_framework import status

from recipes.models import IngredientRecipe


def get_send_file(user):
    """ файл для скачивания"""
    filename = f'Список покупок: {user}.csv'
    if user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    ingredients = IngredientRecipe.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount')).values_list(
        'ingredient__name', 'ingredient__measurement_unit',
        'ingredient_amount')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for item in list(ingredients):
        writer.writerow(item)
    return response
