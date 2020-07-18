# Generated by Django 3.0.8 on 2020-07-14 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_book_book_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_first_name', models.CharField(max_length=20)),
                ('shipping_last_name', models.CharField(max_length=20)),
                ('shipping_house_no', models.CharField(max_length=10)),
                ('shipping_address_one', models.CharField(max_length=50)),
                ('shipping_address_two', models.CharField(blank=True, max_length=50)),
                ('shipping_city', models.CharField(max_length=50)),
                ('shipping_state', models.CharField(max_length=20)),
                ('shipping_country', models.CharField(max_length=20)),
                ('shipping_zip', models.CharField(max_length=10)),
                ('shipping_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]