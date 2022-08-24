from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создаем теги'

    def handle(self, *args, **options):
        data = [
            {'name': 'Завтрак', 'color': '#b39f7a', 'slug': 'desayuno'},
            {'name': 'Обед', 'color': '#7fff00', 'slug': 'almuerzo'},
            {'name': 'Ужин', 'color': '#d2691e', 'slug': 'cena'},
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все теги загружены!'))
