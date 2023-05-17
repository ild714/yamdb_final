from django.core.management.base import BaseCommand
import io
import csv
from reviews.models import (
    Genre, Category, Comment, GenreTitle, Review, YaMdbUser, Title
)


class Command(BaseCommand):

    def users_load(self):
        with io.open('static/data/users.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                review = YaMdbUser(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3]
                )
                review.save()

    def genre_load(self):
        with io.open('static/data/genre.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                user = Genre(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
                user.save()

    def category_load(self):
        path = 'static/data/category.csv'
        with io.open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                category = Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
                category.save()

    def title_load(self):
        with io.open('static/data/titles.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                title = Title(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(pk=row[3])
                )
                title.save()

    def genre_title_load(self):
        path = 'static/data/genre_title.csv'
        with io.open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                genre_title = GenreTitle(
                    id=row[0],
                    title=Title.objects.get(pk=row[1]),
                    genre=Genre.objects.get(pk=row[2])
                )
                genre_title.save()

    def review_load(self):
        with io.open('static/data/review.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                review = Review(
                    id=row[0],
                    title=Title.objects.get(pk=row[1]),
                    text=row[2],
                    author=YaMdbUser.objects.get(pk=row[3]),
                    score=row[4],
                    pub_date=row[5]
                )
                review.save()

    def comments_load(self):
        path = 'static/data/comments.csv'
        with io.open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                comment = Comment(
                    id=row[0],
                    review=Review.objects.get(pk=row[1]),
                    text=row[2],
                    author=YaMdbUser.objects.get(pk=row[3]),
                    pub_date=row[4]
                )
                comment.save()

    def handle(self, *args, **options):
        self.users_load()
        self.genre_load()
        self.category_load()
        self.title_load()
        self.genre_title_load()
        self.review_load()
        self.comments_load()
