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
    owner = models.ForeignKey('CustomUser', verbose_name='Пользователь',
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
    owner = models.ForeignKey('CustomUser', verbose_name='Пользователь',
                              on_delete=models.CASCADE)
    categories = models.ManyToManyField(UserCategory,
                                        related_name='cards')

    class Meta:
        ordering = ('en_word',)

    def __str__(self):
        return f'{self.status}: {self.ru_word} - {self.en_word}'


class UserManager(models.Manager):
    """К новому юзеру должны быть прикреплены все базовые категории о
    карточки слов"""
    def _create_user_related_objs(self, user):
        """Создаются изначальные карточки для юзера"""
        new_categories = [UserCategory(name=basic_category.name,
                                       slug=basic_category.slug,
                                       owner=user)
                          for basic_category in BasicCategory.objects.all(
            ).order_by('id')[0:2]
                          ]
        UserCategory.objects.bulk_create(new_categories,
                                         batch_size=999)

        new_cards = [UserCard(ru_word=basic_card.ru_word,
                              en_word=basic_card.en_word,
                              transcription=basic_card.transcription,
                              owner=user)
                     for basic_card in BasicCard.objects.all()
                     ]
        UserCard.objects.bulk_create(new_cards, batch_size=999)

    def _add_card_category_m2m_relateship(self, user):
        """Связываю созданные карточки и категории, основываясь на связи
        базовых категорий и карточек"""
        user_categories = UserCategory.objects.filter(owner=user)
        user_cards = UserCard.objects.filter(owner=user)
        relates = []
        for category in user_categories:
            matched_cards = BasicCategory.objects.get(
                slug=category.slug).cards.values()
            for card in user_cards:
                for matched_card in matched_cards:
                    if card.ru_word == matched_card['ru_word'] and \
                            card.en_word == matched_card['en_word']:
                        category_card_relate = UserCard.categories.through(
                            usercard_id=card.id, usercategory_id=category.id)
                        relates.append(category_card_relate)
        UserCard.categories.through.objects.bulk_create(relates,
                                                        batch_size=999)

    def create(self, *args, **kwargs):
        new_user = super(UserManager, self).create(*args, **kwargs)
        self._create_user_related_objs(new_user)
        self._add_card_category_m2m_relateship(new_user)


# from learn.models import CustomUser
# c = CustomUser.objects.create(username='greee',password='greee1223')


class CustomUser(User):
    objects = UserManager()
