# Generated by Django 3.2 on 2021-04-20 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210419_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]