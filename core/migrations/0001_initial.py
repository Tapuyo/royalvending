# Generated by Django 5.0.1 on 2025-07-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('product_link', models.URLField()),
                ('current_price', models.CharField(max_length=50)),
                ('carton_price', models.CharField(blank=True, max_length=50)),
                ('single_price', models.CharField(blank=True, max_length=50)),
                ('category', models.CharField(max_length=100)),
                ('item_code', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
