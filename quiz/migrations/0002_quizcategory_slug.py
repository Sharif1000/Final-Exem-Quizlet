# Generated by Django 5.0.2 on 2024-04-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizcategory',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
