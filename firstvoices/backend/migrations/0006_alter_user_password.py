# Generated by Django 4.1.7 on 2023-04-17 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
