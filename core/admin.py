from django.contrib import admin
from .models import *
from .models import User, Contract, Payment, Delivery

admin.site.register(User)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(Delivery)
 