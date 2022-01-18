from django.db import models
from pytils.translit import slugify
from django.contrib.auth.models import User


class BasicCategory(models.Model):
    """Изначальные категории для новых и неавторизованным пользователям"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BasicCard(models.Model):
    """Изначальные карточки слов для новых и неавторизованным пользователям"""
    en_word = models.CharField(max_length=100)
    ru_word = models.CharField(max_length=100)
    transcription = models.CharField(max_length=50, null=True)
    examples = models.JSONField(null=True)
    status = models.CharField(max_length=25, null=True, default='New word')
    count_repeated = models.IntegerField(null=True, default=0)
    categories = models.ManyToManyField(BasicCategory,
                                        related_name='cards')

    class Meta:
        ordering = ('en_word', 'status')

    def __str__(self):
        return f'{self.ru_word} - {self.en_word}'


class UserCategory(models.Model):
    """Модель категории, к которой может относиться карточка для изучения"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    owner = models.ForeignKey(User, verbose_name='Пользователь',
                              default=1,
                              on_delete=models.CASCADE)

    class Meta:
        unique_together = ('owner', 'slug')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(UserCategory, self).save(*args, **kwargs)


class UserCard(models.Model):
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
    transcription = models.CharField(max_length=50, null=True)
    examples = models.JSONField(null=True)
    status = models.CharField(max_length=25,
                              choices=card_statuses,
                              default=new_word_status)

    count_repeated = models.IntegerField(null=True, default=0)
    categories = models.ManyToManyField(UserCategory,
                                        related_name='cards')

    class Meta:
        ordering = ('en_word',)

    def __str__(self):
        return f'{self.status}: {self.ru_word} - {self.en_word}'


class UserManager(models.Manager):
    """К новому юзеру должны быть прикреплены все базовые категории о
    карточки слов"""

    def create(self, *args, **kwargs):
        new_user = super(UserManager, self).create(*args, **kwargs)

        user_categories = [UserCategory(name=basic_category.name,
                                        slug=basic_category.slug,
                                        owner=new_user.id)
                           for basic_category in BasicCategory.objects.all()
                           ]
        UserCategory.objects.bulk_create(user_categories, batch_size=999)

        # for basic_card in BasicCard.objects.all():
        #     user_card = UserCard.objects.create(
        #         ru_word=basic_card.ru_word,
        #         en_word=basic_card.en_word,
        #         transcription=basic_card.transcription,
        #         examples=basic_card.examples)

            # user_card.categories.through(user_card_id=user_card.id,
            #                              user_category_id=)
        # UserCategory.


class CustomUser(User):
    objects = UserManager()
