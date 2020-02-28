# Generated by Django 2.2.10 on 2020-02-28 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokemon', '0001_initial'),
        ('battles', '0003_auto_20200228_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='BattleTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='battles.Battle')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to=settings.AUTH_USER_MODEL)),
                ('pokemon_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='pokemon.Pokemon')),
                ('pokemon_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='pokemon.Pokemon')),
                ('pokemon_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='pokemon.Pokemon')),
            ],
        ),
    ]