from django.db import models


class Machine(models.Model):

    STATUS_CHOICES = [
        ('running', 'En marcha'),
        ('stopped', 'Detenida'),
        ('maintenance', 'Mantenimiento'),
    ]

    name = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='stopped'
    )

    product_name = models.CharField(max_length=100)

    product_weight = models.CharField(max_length=20)

    production_rate_per_sec = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Operator(models.Model):

    SHIFT_CHOICES = [
        ('morning', 'Mañana'),
        ('afternoon', 'Tarde'),
        ('night', 'Noche'),
    ]

    name = models.CharField(max_length=100)

    shift = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES
    )

    def __str__(self):
        return self.name


class ProductionRecord(models.Model):

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.machine.name} - {self.quantity}"


class Event(models.Model):

    EVENT_TYPE_CHOICES = [
        ('maintenance', 'Mantenimiento'),
        ('manual_stop', 'Detención manual'),
    ]

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES
    )

    start_time = models.DateTimeField(auto_now_add=True)

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.machine.name} - {self.event_type}"
    
class Alarm(models.Model):

    ALARM_TYPES = [
        ('jam', 'Atasco de producto'),
        ('sensor', 'Sensor sin respuesta'),
        ('paper', 'Papel no detectado'),
    ]

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )

    alarm_type = models.CharField(
        max_length=20,
        choices=ALARM_TYPES
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine.name} - {self.get_alarm_type_display()}"