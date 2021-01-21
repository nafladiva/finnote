from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Transaksi)
admin.site.register(Tanggungan)
admin.site.register(SaldoUser)