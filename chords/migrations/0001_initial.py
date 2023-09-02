# Generated by Django 4.2.4 on 2023-09-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='title')),
                ('artist', models.CharField(blank=True, db_index=True, max_length=200, verbose_name='artist')),
                ('key', models.CharField(blank=True, max_length=50, verbose_name='key')),
                ('time', models.PositiveIntegerField(blank=True, help_text='Beat per minute', null=True, verbose_name='time')),
                ('tempo', models.CharField(blank=True, help_text='Signature. Eg. 4/4', max_length=50, verbose_name='tempo')),
                ('year', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='year')),
                ('chords', models.TextField(blank=True, help_text='ChordPro format.', verbose_name='chords')),
            ],
            options={
                'verbose_name': 'song',
                'verbose_name_plural': 'songs',
                'ordering': ['title'],
            },
        ),
    ]
