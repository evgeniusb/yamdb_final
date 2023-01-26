import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Genre

FILE2IMPORT = os.path.join(settings.STATICFILES_DIRS[0], 'data/genre.csv')


class Command(BaseCommand):
    help = 'load genre from csv'

    def handle(self, *args, **options):
        with open(FILE2IMPORT, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                genre = Genre(
                    id=id,
                    name=name,
                    slug=slug
                )
                genre.save()
