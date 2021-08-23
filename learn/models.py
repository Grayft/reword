from django.db import models


class CardCategory(models.Model):
    """Модель категории, к которой может относиться карточка для изучения"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Card(models.Model):
    """Модель карточки для изучения слова, фразы."""

    new_word_status = 'New word'
    card_statuses = [(new_word_status, 'Новое слово'),
                     ('Learning word', 'Заучивается'),
                     ('Repeating word', 'Повторение'),
                     ('Learned word', 'Полностью выучено'),
                     ('Known word', 'Уже известно'),
                     ]

    ru_word = models.CharField(max_length=100)
    en_word = models.CharField(max_length=100)
    status = models.CharField(max_length=25,
                              choices=card_statuses,
                              default=new_word_status)
    categories = models.ManyToManyField(CardCategory, related_name='categories')
    repeated_count = models.IntegerField(verbose_name='Количество повторений',
                                         max_length=1, default=0)

    def __str__(self):
        return f'{self.status}: {self.ru_word} - {self.en_word}'


class CardStatistic(models.Model):
    pass
