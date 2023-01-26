import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Review, User

FILE2IMPORT = os.path.join(settings.STATICFILES_DIRS[0], 'data/review.csv')


class Command(BaseCommand):
    help = 'load reviews from csv'

    def handle(self, *args, **options):
        with open(FILE2IMPORT, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                text = row['text']
                author = User.objects.get(id=row['author'])
                score = row['score']
                pub_date = row['pub_date']
                reviews = Review(
                    id=id,
                    title_id=title_id,
                    text=text,
                    author=author,
                    score=score,
                    pub_date=pub_date
                )
                reviews.save()
