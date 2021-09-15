from django.db import models


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, default='')
    name_fr = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    poster = models.CharField(max_length=200, null=True)
    adult = models.BooleanField()
    overview = models.TextField()
    release_date = models.DateField()
    original_title = models.CharField(max_length=200)
    original_language = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f"{self.title} ({self.release_date.year})"

    class Meta:
        ordering = ['-release_date']

