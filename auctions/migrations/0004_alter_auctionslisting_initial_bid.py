# Generated by Django 5.1.2 on 2024-11-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionslisting_initial_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionslisting',
            name='initial_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
