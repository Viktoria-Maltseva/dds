# Generated by Django 5.0.3 on 2025-03-28 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0002_categories_type_operation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dds',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
