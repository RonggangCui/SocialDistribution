# Generated by Django 4.1.7 on 2023-03-02 20:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('app', '0014_inbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inbox',
            name='post',
        ),
        migrations.RemoveField(
            model_name='inbox',
            name='type',
        ),
        migrations.AddField(
            model_name='inbox',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('post', 'post'), ('comment', 'comment')], max_length=10)),
                ('object_id', models.UUIDField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='app.author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('comment', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.post')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('post', 'post'), ('comment', 'comment'), ('follow', 'follow'), ('like', 'like')], max_length=10)),
                ('object_id', models.UUIDField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddField(
            model_name='inbox',
            name='object',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox_item', to='app.activity'),
        ),
    ]
