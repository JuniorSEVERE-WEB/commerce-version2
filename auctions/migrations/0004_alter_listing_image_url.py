# Generated by Django 5.2.3 on 2025-07-01 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_image_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Image URL'),
        ),
    ]
