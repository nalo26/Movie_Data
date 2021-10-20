from django.db import models


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, default='')
    name_fr = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name

class Production_Country(models.Model):
    iso = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)

class Production_Company(models.Model):
    id = models.IntegerField(primary_key=True)
    logo = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200)
    origin_country = models.CharField(max_length=200)

class Spoken_Languages(models.Model):
    iso = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=10, default="")
    poster = models.CharField(max_length=200, default="")
    adult = models.BooleanField()
    overview = models.TextField()
    release_date = models.DateField()
    original_title = models.CharField(max_length=200)
    original_language = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    budget = models.BigIntegerField(default=0)
    revenue = models.BigIntegerField(default=0)
    runtime = models.IntegerField(default=0)
    status = models.CharField(max_length=200, default="")
    tagline = models.TextField(default="")
    genres = models.ManyToManyField(Genre)
    production_companies = models.ManyToManyField(Production_Company)
    production_countries = models.ManyToManyField(Production_Country)
    spoken_languages = models.ManyToManyField(Spoken_Languages)

    def __str__(self):
        return f"{self.title} ({self.release_date.year})"

    class Meta:
        ordering = ['-release_date']

