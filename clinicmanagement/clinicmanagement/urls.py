from django.contrib import admin
from django.urls import path
from clinic import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('dentistclick', views.dentistclick_view),
    path('patientclick', views.patientclick_view),

    path('adminsignup', views.admin_signup_view),
    path('dentistignup', views.dentist_signup_view,name='dentistsignup'),
    path('patientsignup', views.patient_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='clinic/adminlogin.html')),
    path('dentistlogin', LoginView.as_view(template_name='clinic/dentistlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='clinic/patientlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='clinic/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-dentist', views.admin_dentist_view,name='admin-dentist'),
    path('admin-view-dentist', views.admin_view_dentist_view,name='admin-view-dentist'),
    path('delete-dentist-from-clinic/<int:pk>', views.delete_dentist_from_clinic_view,name='delete-dentist-from-clinic'),
    path('update-dentist/<int:pk>', views.update_dentist_view,name='update-dentist'),
    path('admin-add-dentist', views.admin_add_dentist_view,name='admin-add-dentist'),
    path('admin-approve-dentist', views.admin_approve_dentist_view,name='admin-approve-dentist'),
    path('approve-dentist/<int:pk>', views.approve_dentist_view,name='approve-dentist'),
    path('reject-dentist/<int:pk>', views.reject_dentist_view,name='reject-dentist'),
    path('admin-view-dentist-specialisation',views.admin_view_dentist_specialisation_view,name='admin-view-dentist-specialisation'),


    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-clinic/<int:pk>', views.delete_patient_from_clinic_view,name='delete-patient-from-clinic'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR dentist RELATED URLS-------------------------------------
urlpatterns +=[
    path('dentist-dashboard', views.dentist_dashboard_view,name='dentist-dashboard'),
    path('search', views.search_view,name='search'),

    path('dentist-patient', views.dentist_patient_view,name='dentist-patient'),
    path('dentist-view-patient', views.dentist_view_patient_view,name='dentist-view-patient'),
    path('dentist-view-discharge-patient',views.dentist_view_discharge_patient_view,name='dentist-view-discharge-patient'),

    path('dentist-appointment', views.dentist_appointment_view,name='dentist-appointment'),
    path('dentist-view-appointment', views.dentist_view_appointment_view,name='dentist-view-appointment'),
    path('dentist-delete-appointment',views.dentist_delete_appointment_view,name='dentist-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-dentist', views.patient_view_dentist_view,name='patient-view-dentist'),
    path('searchdentist', views.search_dentist_view,name='searchdentist'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]


