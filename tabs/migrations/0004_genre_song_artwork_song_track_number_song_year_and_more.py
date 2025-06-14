# Generated by Django 5.2.2 on 2025-06-08 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0003_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='artwork',
            field=models.ImageField(blank=True, null=True, upload_to='artwork/'),
        ),
        migrations.AddField(
            model_name='song',
            name='track_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='gpx_file',
            field=models.FileField(blank=True, null=True, upload_to='gpx/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='mp3_file',
            field=models.FileField(upload_to='tracks/'),
        ),
        migrations.AddField(
            model_name='song',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='songs', to='tabs.genre'),
        ),
    ]
