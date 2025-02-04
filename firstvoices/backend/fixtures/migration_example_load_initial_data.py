# Generated by Django 4.1.7 on 2023-03-30 17:18
# Migration file to load initial data for PartOfSpeech model
# To include Categories and possibly other models in the future
# See both answers by @djvg and @Rockallite in the following link
# Ref: https://stackoverflow.com/questions/25960850/loading-initial-data-with-django-1-7-and-data-migrations

# The following code can be added in a migration to automate the adding of data from this fixture.
# Commented out till we commit migrations to commit this later.

# from django.db import migrations
# from django.core.serializers import base, python
# from django.core.management import call_command
#
#
# def load_fixture(apps, schema_editor):
#     old_get_model = python._get_model
#
#     def _get_model(model_identifier):
#         try:
#             return apps.get_model(model_identifier)
#         except (LookupError, TypeError):
#             raise base.DeserializationError("Invalid model identifier: '%s'" % model_identifier)
#
#     python._get_model = _get_model
#
#     try:
#         call_command('loaddata', 'partsOfSpeech_initial.json', app_label="backend")
#     finally:
#         python._get_model = old_get_model
#
#
# class Migration(migrations.Migration):
#     dependencies = []
#
#     operations = [
#         migrations.RunPython(load_fixture),
#     ]
