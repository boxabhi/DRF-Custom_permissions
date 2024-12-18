from django.contrib import admin

# Register your models here.

from .models import Store,StoreOwner


admin.site.register(Store)
admin.site.register(StoreOwner)

