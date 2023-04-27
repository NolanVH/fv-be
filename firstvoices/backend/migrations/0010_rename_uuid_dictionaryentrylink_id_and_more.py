# Generated by Django 4.1.7 on 2023-04-24 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0009_remove_dictionaryentrylink_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dictionaryentrylink",
            old_name="uuid",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="dictionaryentryrelatedcharacter",
            old_name="uuid",
            new_name="id",
        ),
        migrations.AddField(
            model_name="dictionaryentrylink",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dictionaryentrylink",
            name="created_by",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="dictionaryentrylink",
            name="is_trashed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="dictionaryentrylink",
            name="last_modified",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name="dictionaryentrylink",
            name="last_modified_by",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="modified_%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="dictionaryentryrelatedcharacter",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dictionaryentryrelatedcharacter",
            name="created_by",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="dictionaryentryrelatedcharacter",
            name="is_trashed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="dictionaryentryrelatedcharacter",
            name="last_modified",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name="dictionaryentryrelatedcharacter",
            name="last_modified_by",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="modified_%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
