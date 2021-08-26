from django.db import models
from pytils.translit import slugify
from django.contrib.auth.models import User


class CardCategory(models.Model):
    """Модель категории, к которой может относиться карточка для изучения"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    owner = models.ForeignKey(User, verbose_name='Пользователь',
                              default=1,
                              on_delete=models.CASCADE)

    class Meta:
        unique_together = ('owner', 'slug')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(CardCategory, self).save(*args, **kwargs)


class Card(models.Model):
    """Модель карточки для изучения слова, фразы.
    Все взаимодействие с карточками происходит через категории,
    поэтому Card не имеет поле owner"""

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
    categories = models.ManyToManyField(CardCategory,
                                        related_name='categories')
    remain_repeated_count = models.IntegerField(
        verbose_name='Количество повторений',
        default=6)

    def __str__(self):
        return f'{self.status}: {self.ru_word} - {self.en_word}'


class CardStatistic(models.Model):
    pass
