# Generated by Django 3.2.6 on 2021-08-23 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CardStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ru_word', models.CharField(max_length=100)),
                ('en_word', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('New word', 'Новое слово'), ('Learning word', 'Заучивается'), ('Repeating word', 'Повторение'), ('Learned word', 'Полностью выучено'), ('Known word', 'Уже известно')], default='New word', max_length=25)),
                ('repeated_count', models.IntegerField(default=0, max_length=1, verbose_name='Количество повторений')),
                ('categories', models.ManyToManyField(related_name='categories', to='learn.CardCategory')),
            ],
        ),
    ]
