# Generated by Django 5.0.2 on 2024-04-13 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('quiz', '0002_quizcategory_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('reviewer', 'quiz')},
        ),
    ]