# Generated by Django 2.2.10 on 2020-03-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0008_battle_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]