# Generated by Django 2.2.2 on 2019-07-22 16:01

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_post_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='topic',
            field=models.IntegerField(),
        ),
    ]