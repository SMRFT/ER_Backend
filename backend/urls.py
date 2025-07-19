from django.urls import path
from . import views 

urlpatterns = [
    path('erbilling/', views.er_billing,name='erbilling'),
    path('erregister/', views.erregister_patient, name='erregister_patient'),
    path('next-bill-number/', views.get_next_bill_number),
    path('dashboard/', views.get_patients_by_date),
    path('erregisteredit/', views.er_register_view),
    path("procedures/", views.get_procedure_list, name="procedure-list"),
    path("doctors/", views.get_doctor_list, name="doctor-list"),
    path('get_er_patients_by_date/', views.get_er_patients_by_date, name='get_er_patients_by_date'),
    path('printbill/', views.fetch_er_patient_bills, name='fetch_er_patient_bills'),
    path('erreports/', views.get_er_reports, name='get_er_reports'),


]
