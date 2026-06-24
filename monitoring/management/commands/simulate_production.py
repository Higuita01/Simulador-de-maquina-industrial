import random
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import Machine, ProductionRecord, Alarm


class Command(BaseCommand):
    help = "Simula producción industrial controlada"

    def handle(self, *args, **kwargs):

        self.stdout.write("🔧 Simulación iniciada...")

        while True:

            machines = Machine.objects.filter(status='running')

            for machine in machines:

                # =========================
                # 📦 PRODUCCIÓN
                # =========================
                ProductionRecord.objects.create(
                    machine=machine,
                    timestamp=timezone.now(),
                    quantity=machine.production_rate_per_sec
                )

                # =========================
                # 🚨 FALLAS (SOLO EVENTO)
                # =========================
                if random.randint(1, 100) <= 2:

                    alarm_type = random.choice([
                        'jam',
                        'sensor',
                        'paper'
                    ])

                    Alarm.objects.create(
                        machine=machine,
                        alarm_type=alarm_type,
                        active=True
                    )

                    self.stdout.write(
                        self.style.ERROR(
                            f"🚨 FALLA EN {machine.name}"
                        )
                    )

            time.sleep(5)