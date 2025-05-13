from django.contrib import admin
from .models import Dentist,Patient,Appointment,PatientDischargeDetails
# Register your models here.
class DentistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Dentist, DentistAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

