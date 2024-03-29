# Generated by Django 3.1.7 on 2021-04-09 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('location', models.CharField(max_length=64)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('www', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created datetime')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('ship', 'Boat'), ('bus', 'Bus'), ('car', 'Car'), ('motorcycle', 'Motorcycle'), ('plane', 'Plane'), ('rocket', 'Rocket'), ('space-shuttle', 'Space Shuttle'), ('train', 'Train')], default='plane', max_length=13)),
                ('departure_town', models.CharField(max_length=64)),
                ('departure_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('departure_datetime', models.DateTimeField()),
                ('arrival_town', models.CharField(max_length=64)),
                ('arrival_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('arrival_datetime', models.DateTimeField()),
                ('detail1', models.CharField(blank=True, max_length=32, null=True)),
                ('detail2', models.CharField(blank=True, max_length=32, null=True)),
                ('towards_home', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='party.party')),
            ],
        ),
    ]
