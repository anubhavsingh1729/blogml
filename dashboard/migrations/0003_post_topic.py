# Generated by Django 2.2.2 on 2019-07-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190717_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.CharField(default=-1, max_length=10),
        ),
    ]