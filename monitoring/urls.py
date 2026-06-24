from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('api/kpis/', views.kpi_data, name='kpi_data'),

    path(
        'machine/<int:machine_id>/status/',
        views.update_machine_status,
        name='update_machine_status'
    ),

    path(
        'machine/<int:machine_id>/reset/',
        views.reset_machine_alarm,
        name='reset_machine_alarm'
    ),

    path(
        'api/state/',
        views.machines_state,
        name='machines_state'
    ),
]