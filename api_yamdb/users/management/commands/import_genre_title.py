import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import TitleGenre

FILE2IMPORT = os.path.join(
    settings.STATICFILES_DIRS[0],
    'data/genre_title.csv'
)


class Command(BaseCommand):
    help = 'load genre_titles from csv'

    def handle(self, *args, **options):
        with open(FILE2IMPORT, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']

                title_id = row['title_id']
                genre_id = row['genre_id']
                title_genres = TitleGenre(
                    id=id,
                    title_id=title_id,
                    genre_id=genre_id
                )
                title_genres.save()
