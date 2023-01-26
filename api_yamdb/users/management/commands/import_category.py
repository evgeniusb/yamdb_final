import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category

FILE2IMPORT = os.path.join(settings.STATICFILES_DIRS[0], 'data/category.csv')


class Command(BaseCommand):
    help = 'load category from csv'

    def handle(self, *args, **options):
        with open(FILE2IMPORT, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                category = Category(
                    id=id,
                    name=name,
                    slug=slug
                )
                category.save()
