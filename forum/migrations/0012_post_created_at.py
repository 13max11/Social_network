# Generated by Django 5.1.4 on 2025-01-26 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_community_rule_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
