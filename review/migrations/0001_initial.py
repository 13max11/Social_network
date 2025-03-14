# Generated by Django 5.1.4 on 2025-03-05 18:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/blog/')),
                ('status', models.CharField(choices=[('0', 'не преглянуто'), ('1', 'прийнято'), ('2', 'відхилено')], default='0', max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
