from django.urls import path

from .views import validate_slot_view, validate_numeric_constraint

urlpatterns = [
    path('validate-slot', validate_slot_view, name='validate-slot'),
    path('validate-constraint', validate_numeric_constraint, name='validate_constraint')
]
