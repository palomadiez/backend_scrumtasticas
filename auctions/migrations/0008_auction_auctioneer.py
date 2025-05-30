# Generated by Django 5.1.7 on 2025-04-09 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_auction_auctioneer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auctioneer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
