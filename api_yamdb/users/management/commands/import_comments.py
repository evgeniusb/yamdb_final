import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Comment, User

FILE2IMPORT = os.path.join(settings.STATICFILES_DIRS[0], 'data/comments.csv')


class Command(BaseCommand):
    help = 'load category from csv'

    def handle(self, *args, **options):
        with open(FILE2IMPORT, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            # id,review_id,text,author,pub_date
            for row in csv_reader:
                id = row['id']
                review_id = row['review_id']
                text = row['text']
                author = User.objects.get(id=row['author'])
                pub_date = row['pub_date']
                comment = Comment(
                    id=id,
                    review_id=review_id,
                    text=text,
                    author=author,
                    pub_date=pub_date
                )
                comment.save()
