# Generated by Django 3.0.5 on 2020-05-03 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
