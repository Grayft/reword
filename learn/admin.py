from django.contrib import admin
from .models import UserCard, UserCategory
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    pass


class CardCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserCard, CardAdmin)
admin.site.register(UserCategory, CardCategoryAdmin)