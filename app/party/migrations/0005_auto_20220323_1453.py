# Generated by Django 3.1.7 on 2022-03-23 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('party', '0004_auto_20220323_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_parties', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='party',
            name='modified_dt',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Modified datetime'),
        ),
        migrations.AlterField(
            model_name='party',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_parties', to=settings.AUTH_USER_MODEL),
        ),
    ]