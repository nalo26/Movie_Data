# Generated by Django 3.2.7 on 2021-10-15 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movietut', '0002_alter_movie_tagline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.BigIntegerField(default=0),
        ),
    ]
