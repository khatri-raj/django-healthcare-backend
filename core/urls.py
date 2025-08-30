from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # API URLs
    path('api/auth/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/auth/login/', views.LoginView.as_view(), name='api_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/patients/', views.PatientListCreateView.as_view(), name='api_patients'),
    path('api/patients/<int:pk>/', views.PatientDetailView.as_view(), name='api_patient_detail'),
    path('api/doctors/', views.DoctorListCreateView.as_view(), name='api_doctors'),
    path('api/doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='api_doctor_detail'),
    # Patient-doctor mappings
    path('api/mappings/', views.MappingListCreateView.as_view(), name='api_mappings'),
    path('api/mappings/patient/<int:patient_id>/', views.MappingPatientDoctorsView.as_view(), name='api_patient_mappings'),
    path('api/mappings/<int:pk>/delete/', views.MappingDeleteView.as_view(), name='api_mapping_delete'),

    # Template URLs
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patients/', views.patient_list_view, name='patient_list'),
    path("patients/<int:pk>/update/", views.patient_update_view, name="patient_update"),
    path('patients/delete/<int:pk>/', views.patient_delete_view, name='patient_delete'),
    path('doctors/', views.doctor_list_view, name='doctor_list'),
    path("doctors/<int:pk>/update/", views.doctor_update_view, name="doctor_update"),
    path('doctors/delete/<int:pk>/', views.doctor_delete_view, name='doctor_delete'),
    path('mappings/', views.mapping_list_view, name='mapping_list'),
    path('mappings/delete/<int:pk>/', views.mapping_delete_view, name='mapping_delete'),
]