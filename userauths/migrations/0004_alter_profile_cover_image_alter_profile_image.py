# Generated by Django 5.0.6 on 2024-05-22 07:39

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_alter_profile_cover_image_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/ddfsqd1ru/image/upload/v1715963028/kenh9ewa1adngh4yyeoc.jpg', max_length=255, null=True, verbose_name='cover_image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/ddfsqd1ru/image/upload/v1715963029/jjalhv4zektgahhxj6yw.jpg', max_length=255, null=True, verbose_name='image'),
        ),
    ]
