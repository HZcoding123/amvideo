# Generated by Django 3.2.8 on 2022-06-15 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='视频时长'),
        ),
    ]