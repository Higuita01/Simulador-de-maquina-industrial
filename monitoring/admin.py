from django.contrib import admin
from .models import (
    Machine,
    Operator,
    ProductionRecord,
    Event,
    Alarm
)

admin.site.register(Machine)
admin.site.register(Operator)
admin.site.register(ProductionRecord)
admin.site.register(Event)
admin.site.register(Alarm)