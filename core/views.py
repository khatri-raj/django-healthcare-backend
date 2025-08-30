from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer, PatientSerializer, DoctorSerializer,
    MappingSerializer, MyTokenObtainPairSerializer
)
from .forms import RegisterForm, LoginForm, PatientForm, DoctorForm, MappingForm

# API Views (for RESTful endpoints)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(user=self.request.user)

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class MappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

class MappingPatientDoctorsView(generics.ListAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        if self.request.user.is_superuser:
            return PatientDoctorMapping.objects.filter(patient_id=patient_id)
            # normal user must own the patient
        Patient.objects.get(id=patient_id, user=self.request.user)
        return PatientDoctorMapping.objects.filter(patient_id=patient_id, patient__user=self.request.user)


class MappingDeleteView(generics.DestroyAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__user=self.request.user)

# Template Views (for web interface)
def home_view(request):
    return render(request, "core/home.html")

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_list')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('patient_list')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def patient_list_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    patients = Patient.objects.filter(user=request.user)
    return render(request, 'core/patient_list.html', {'patient_form': form, 'patients': patients})

@login_required
def patient_delete_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk, user=request.user)
    patient.delete()
    return redirect('patient_list')

@login_required
def patient_update_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'core/patient_update.html', {'patient_form': form, 'patient': patient})

@login_required
def doctor_list_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    doctors = Doctor.objects.all()
    return render(request, 'core/doctor_list.html', {'doctor_form': form, 'doctors': doctors})

@login_required
def doctor_delete_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    return redirect('doctor_list')

@login_required
def doctor_update_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'core/doctor_update.html', {'doctor_form': form, 'doctor': doctor})

@login_required
def mapping_list_view(request):
    if request.method == 'POST':
        form = MappingForm(request.POST, user=request.user)
        if form.is_valid():
            mapping = form.save(commit=False)
            if mapping.patient.user == request.user:
                mapping.save()
                return redirect('mapping_list')
            else:
                form.add_error(None, "You can only assign doctors to your own patients.")
    else:
        form = MappingForm(user=request.user)
    if request.user.is_superuser:
        mappings = PatientDoctorMapping.objects.all()
    else:
        mappings = PatientDoctorMapping.objects.filter(patient__user=request.user)
    return render(request, 'core/mapping_list.html', {'mapping_form': form, 'mappings': mappings})

@login_required
def mapping_delete_view(request, pk):
    mapping = get_object_or_404(PatientDoctorMapping, pk=pk, patient__user=request.user)
    mapping.delete()
    return redirect('mapping_list')