# Generated by Django 5.1.4 on 2025-02-10 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_alter_communitygroup_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitygroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
