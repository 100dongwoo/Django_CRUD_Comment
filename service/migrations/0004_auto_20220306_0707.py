# Generated by Django 3.1.2 on 2022-03-06 07:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20220301_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
