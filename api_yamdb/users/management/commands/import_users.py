import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User

FILE2IMPORT = os.path.join(settings.STATICFILES_DIRS[0], 'data/users.csv')


class Command(BaseCommand):
    help = 'load users from csv'

    def handle(self, *args, **options):
        with open(FILE2IMPORT, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                users = User(
                    id=id,
                    username=username,
                    email=email,
                    role=role,
                    bio=bio,
                    first_name=first_name,
                    last_name=last_name
                )
                users.save()
