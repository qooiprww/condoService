# Generated by Django 3.0.5 on 2021-03-29 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_auto_20210326_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='seedcontainer',
            name='seed_container_name',
            field=models.CharField(default='Seed Container', max_length=255),
        ),
    ]
