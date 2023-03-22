# Generated by Django 4.1.7 on 2023-03-22 21:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import rules.contrib.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=10, unique=True)),
                ("sort_order", models.IntegerField(unique=True)),
                ("approximate_form", models.CharField(blank=True, max_length=10)),
                ("notes", models.TextField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "character",
                "verbose_name_plural": "characters",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=200)),
                ("alternate_names", models.CharField(blank=True, max_length=200)),
                ("language_code", models.CharField(blank=True, max_length=20)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "language",
                "verbose_name_plural": "languages",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Site",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=200)),
                (
                    "slug",
                    models.SlugField(
                        max_length=200,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                    ),
                ),
                (
                    "visibility",
                    models.IntegerField(
                        choices=[(0, "Team"), (1, "Members"), (2, "Public")],
                        db_index=True,
                        default=0,
                    ),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app.language",
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "site",
                "verbose_name_plural": "sites",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SiteFeature",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("key", models.CharField(max_length=100)),
                ("is_enabled", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.site"
                    ),
                ),
            ],
            options={
                "verbose_name": "site feature",
                "verbose_name_plural": "site features",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="LanguageFamily",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=200)),
                ("alternate_names", models.TextField(blank=True, max_length=200)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "language family",
                "verbose_name_plural": "language families",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name="language",
            name="language_family",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="app.languagefamily"
            ),
        ),
        migrations.AddField(
            model_name="language",
            name="last_modified_by",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="modified_%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="IgnoredCharacter",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=10, unique=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.site"
                    ),
                ),
            ],
            options={
                "verbose_name": "ignored character",
                "verbose_name_plural": "ignored characters",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="CharacterVariant",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("title", models.CharField(max_length=10, unique=True)),
                (
                    "base_character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="app.character",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.site"
                    ),
                ),
            ],
            options={
                "verbose_name": "character variant",
                "verbose_name_plural": "character variants",
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name="character",
            name="site",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.site"
            ),
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_trashed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_modified", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "role",
                    models.IntegerField(
                        choices=[
                            (0, "Member"),
                            (1, "Assistant"),
                            (2, "Editor"),
                            (3, "Language Admin"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_%(app_label)s_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.site"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "membership",
                "verbose_name_plural": "memberships",
                "unique_together": {("site", "user")},
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
