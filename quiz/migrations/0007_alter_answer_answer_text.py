# Generated by Django 5.0.4 on 2024-04-15 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_rename_text_answer_answer_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
