# Generated by Django 4.1.2 on 2022-10-19 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0007_auto_20220329_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='type',
            field=models.CharField(choices=[('bicycle', 'Bicycle'), ('ship', 'Boat'), ('bus', 'Bus'), ('car', 'Car'), ('motorcycle', 'Motorcycle'), ('plane', 'Plane'), ('train', 'Train'), ('walking', 'Walking'), ('other', 'Other')], default='plane', max_length=13),
        ),
    ]
