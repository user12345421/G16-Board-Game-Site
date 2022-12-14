# Generated by Django 4.1.3 on 2022-12-08 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("boardgame_site", "0002_boardgame_summary"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lending",
            name="lent_game",
        ),
        migrations.AddField(
            model_name="boardgame",
            name="lending_obj",
            field=models.ManyToManyField(to="boardgame_site.lending"),
        ),
        migrations.AlterField(
            model_name="boardgame",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
