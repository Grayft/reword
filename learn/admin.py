from django.contrib import admin
from .models import Card, CardCategory
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    pass


class CardCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Card, CardAdmin)
admin.site.register(CardCategory, CardCategoryAdmin)