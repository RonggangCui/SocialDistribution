# Generated by Django 4.1.7 on 2023-03-03 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_merge_20230303_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('text/markdown', 'markdown'), ('text/plain', 'plain'), ('image/png', 'image-png'), ('image/jpeg', 'image-jpeg')], max_length=18),
        ),
    ]
