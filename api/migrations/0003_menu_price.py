# Generated by Django 4.0.4 on 2022-04-14 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_menu_stock_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='price',
            field=models.PositiveIntegerField(default=3000),
        ),
    ]
