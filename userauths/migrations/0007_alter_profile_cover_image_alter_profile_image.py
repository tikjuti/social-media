# Generated by Django 5.0.6 on 2024-05-22 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0006_alter_profile_cover_image_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_image',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/ddfsqd1ru/image/upload/v1715963028/kenh9ewa1adngh4yyeoc.jpg', max_length=255, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/ddfsqd1ru/image/upload/v1715963029/jjalhv4zektgahhxj6yw.jpg', max_length=255, null=True, upload_to=''),
        ),
    ]
