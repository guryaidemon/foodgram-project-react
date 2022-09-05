import csv

from django.core.management import BaseCommand

from foodgram import settings
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR
        with open(f'{data_path}/data/ingredients.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            Ingredient.objects.all().delete
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(name=name, measurement_unit=unit)
        print('Загрузка завершена')
