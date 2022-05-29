from django.contrib import admin
from bank.models import Face, MoneyTransfer, UserAccount
# Register your models here.

admin.site.register(Face)
admin.site.register(MoneyTransfer)
admin.site.register(UserAccount)
