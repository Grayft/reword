from django.db import models
from pytils.translit import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


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
                              on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False, blank=True)

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
    owner = models.ForeignKey(User, verbose_name='Пользователь',
                              on_delete=models.CASCADE)
    categories = models.ManyToManyField(UserCategory,
                                        related_name='cards')

    class Meta:
        ordering = ('en_word',)

    def __str__(self):
        return f'{self.status}: {self.ru_word} - {self.en_word}'


def _create_user_related_objs(user):
    """Создаются изначальные карточки для юзера"""
    new_categories = [UserCategory(name=basic_category.name,
                                   slug=basic_category.slug,
                                   owner=user)
                      for basic_category in BasicCategory.objects.all()
            #           BasicCategory.objects.filter(
            # id__in=[2, 8, 10, 12, 13, 14,3,4,5,6,7,9,15,16,17,18,18,19,20])
                      ]
    UserCategory.objects.bulk_create(new_categories,
                                     batch_size=999)

    new_cards = [UserCard(ru_word=basic_card.ru_word,
                          en_word=basic_card.en_word,
                          transcription=basic_card.transcription,
                          owner=user)
                 for basic_card in BasicCard.objects.all()
            #      BasicCard.objects.filter(
            # categories__id__in=[2, 8, 10, 12, 13, 14,3,4,5,6,7,9,15,16,17,18,18,19,20])
                 ]
    UserCard.objects.bulk_create(new_cards, batch_size=999)


def _add_card_category_m2m_relation(user):
    """Связываю созданные карточки и категории, основываясь на связи
    базовых категорий и карточек"""
    user_categories = UserCategory.objects.filter(owner=user)
    user_cards = UserCard.objects.filter(owner=user)

    for category in user_categories:
        relates = []
        matched_cards = BasicCategory.objects.get(
            slug=category.slug).cards.values()
        for card in user_cards:
            try:
                # если карточка и категория не соответствуют,
                # то вылетает ошибка и идем дальше
                matched_card = BasicCard.objects.get(
                    categories__slug=category.slug, ru_word=card.ru_word,
                    en_word=card.en_word)

                category_card_relate = UserCard.categories.through(
                    usercard_id=card.id, usercategory_id=category.id)
                relates.append(category_card_relate)
            except ObjectDoesNotExist:
                pass
        # Выполняю bulk_create для каждой категории, т.к. если одним запросом
        # все связи добавлять (17000 строк), то SQLite не заносит их вообще
        # даже с batch_size=999
        UserCard.categories.through.objects.bulk_create(relates,
                                                        batch_size=999)


@receiver(post_save, sender=User)
def create_user_related_data(sender, instance, created, **kwargs):
    if created:
        try:
            _create_user_related_objs(instance)
            _add_card_category_m2m_relation(instance)
        except:
            pass
