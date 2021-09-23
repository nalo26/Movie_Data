import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
                ('name_fr', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Production_Company',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('logo', models.CharField(default='', max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('origin_country', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Production_Country',
            fields=[
                ('iso', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Spoken_Languages',
            fields=[
                ('iso', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('imdb_id', models.CharField(default='', max_length=10)),
                ('poster', models.CharField(default='', max_length=200)),
                ('adult', models.BooleanField()),
                ('overview', models.TextField()),
                ('release_date', models.DateField()),
                ('original_title', models.CharField(max_length=200)),
                ('original_language', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('popularity', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('budget', models.IntegerField(default=0)),
                ('revenue', models.IntegerField(default=0)),
                ('runtime', models.IntegerField(default=0)),
                ('status', models.CharField(default='', max_length=200)),
                ('tagline', models.CharField(default='', max_length=200)),
                ('genres', models.ManyToManyField(to='movietut.Genre')),
                ('production_companies', models.ManyToManyField(to='movietut.Production_Company')),
                ('production_countries', models.ManyToManyField(to='movietut.Production_Country')),
                ('spoken_languages', models.ManyToManyField(to='movietut.Spoken_Languages')),

            ],
            options={
                'ordering': ['-release_date'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
            options={
                'ordering': ['-release_date'],
            },
        ),
    ]
