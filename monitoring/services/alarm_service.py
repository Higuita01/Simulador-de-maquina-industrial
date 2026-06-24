from monitoring.models import Alarm


def process_active_alarms():

    active_alarms = Alarm.objects.filter(active=True)

    for alarm in active_alarms:

        machine = alarm.machine

        if machine.status == 'running':

            machine.status = 'maintenance'
            machine.save()