from rest_framework import permissions
from .models import Patient, Doctor, PatientDoctorMapping

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Patient):
            return obj.user == request.user
        elif isinstance(obj, Doctor):
            return obj.user == request.user
        elif isinstance(obj, PatientDoctorMapping):
            return obj.patient.user == request.user
        return False