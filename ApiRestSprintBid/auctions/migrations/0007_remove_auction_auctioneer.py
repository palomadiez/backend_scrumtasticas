# Generated by Django 5.1.7 on 2025-04-09 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_auctioneer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='auctioneer',
        ),
    ]
