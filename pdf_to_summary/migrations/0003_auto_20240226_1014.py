# Generated by Django 3.2.10 on 2024-02-26 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_to_summary', '0002_auto_20240222_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdfdocument',
            name='user1',
        ),
        migrations.AlterField(
            model_name='pdfdocument',
            name='pages_to_summarize',
            field=models.CharField(max_length=20),
        ),
    ]