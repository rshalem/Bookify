# Generated by Django 3.0.8 on 2020-07-17 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_orderitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='order_item',
            field=models.ManyToManyField(to='main.OrderItem'),
        ),
    ]
