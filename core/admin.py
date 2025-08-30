from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'age', 'gender', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name', 'user__email', 'user__first_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        # Optional: Restrict superusers to see all patients, others to see only their own
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'email', 'contact_number', 'created_at')
    list_filter = ('specialty', 'created_at')
    search_fields = ('name', 'specialty', 'email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('patient__name', 'doctor__name')
    readonly_fields = ('assigned_at',)
    ordering = ('-assigned_at',)

    def get_queryset(self, request):
        # Optional: Restrict to mappings where the patient belongs to the user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(patient__user=request.user)