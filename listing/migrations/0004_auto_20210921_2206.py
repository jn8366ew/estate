# Generated by Django 3.2.7 on 2021-09-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0003_alter_listing_home_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='state',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='zipcode',
            field=models.CharField(max_length=255),
        ),
    ]