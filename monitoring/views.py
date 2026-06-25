from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Machine, Alarm
from django.views.decorators.csrf import ensure_csrf_cookie


from .models import Machine, ProductionRecord, Alarm

@ensure_csrf_cookie
def dashboard(request):
    
    Machine.objects.get_or_create(
    name="Línea Caramelos",
    defaults={
        "status": "stopped",                    
        "product_name": "Caramelos",
        "product_weight": "500g",
        "production_rate_per_sec": 100,
       }
    )
    
    machines = Machine.objects.all()
    now = timezone.now()

    today_production = ProductionRecord.objects.filter(
        timestamp__date=now.date()
    ).aggregate(total=Sum('quantity'))['total'] or 0

    month_production = ProductionRecord.objects.filter(
        timestamp__year=now.year,
        timestamp__month=now.month
    ).aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        'machines': machines,
        'today_production': today_production,
        'month_production': month_production,
    }

    return render(request, 'monitoring/dashboard.html', context)


def kpi_data(request):

    now = timezone.now()

    today_production = ProductionRecord.objects.filter(
        timestamp__date=now.date()
    ).aggregate(total=Sum('quantity'))['total'] or 0

    month_production = ProductionRecord.objects.filter(
        timestamp__year=now.year,
        timestamp__month=now.month
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'today_production': today_production,
        'month_production': month_production
    })

@require_POST
def update_machine_status(request, machine_id):

    machine = get_object_or_404(Machine, id=machine_id)
    status = request.POST.get('status')

    active_alarm = Alarm.objects.filter(
        machine=machine,
        active=True
    ).exists()

    # =========================
    # 🚨 REGLAS INDUSTRIALES
    # =========================

    # ❌ No puede arrancar con alarma
    if active_alarm and status == 'running':
        return JsonResponse({
            'error': 'Máquina bloqueada por alarma activa'
        }, status=400)

    # 🟡 Si pasa a RUNNING, se limpia alarma (override operador)
    if status == 'running':
        Alarm.objects.filter(
            machine=machine,
            active=True
        ).update(active=False)

    # 🔴 lógica de seguridad: si pasa a MAINTENANCE, no puede producir
    if status == 'maintenance':
        machine.status = 'maintenance'
        machine.save()
        return JsonResponse({
            'success': True,
            'status': machine.status
        })

    # 🧠 estado normal
    machine.status = status
    machine.save()

    return JsonResponse({
        'success': True,
        'status': machine.status
    })
    
@require_POST
def reset_machine_alarm(request, machine_id):

    machine = get_object_or_404(Machine, id=machine_id)

    # desactivar alarmas
    Alarm.objects.filter(
        machine=machine,
        active=True
    ).update(active=False)

    # opcional: liberar máquina a stopped o dejarla igual
    if machine.status == 'maintenance':
        machine.status = 'stopped'
        machine.save()

    return JsonResponse({
        'success': True,
        'message': 'Alarmas reseteadas'
    })
    
def machines_state(request):

    machines = list(Machine.objects.values())
    
    alarms = list(
        Alarm.objects.filter(active=True).values(
            'id',
            'machine_id',
            'alarm_type',
            'created_at'
        )
    )

    return JsonResponse({
        "machines": machines,
        "alarms": alarms
    })
