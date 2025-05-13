from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinic/index.html')


#for showing signup/login button for admin 
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinic/adminclick.html')


#for showing signup/login button for dentist
def dentistclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinic/dentistclick.html')


#for showing signup/login button for patient 
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinic/patientclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'clinic/adminsignup.html',{'form':form})




def dentist_signup_view(request):
    userForm=forms.DentistUserForm()
    dentistForm=forms.DentistForm()
    mydict={'userForm':userForm,'dentistForm':dentistForm}
    if request.method=='POST':
        userForm=forms.DentistUserForm(request.POST)
        dentistForm=forms.DentistForm(request.POST,request.FILES)
        if userForm.is_valid() and dentistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            dentist=dentistForm.save(commit=False)
            dentist.user=user
            dentist=dentist.save()
            my_dentist_group = Group.objects.get_or_create(name='Dentist')
            my_dentist_group[0].user_set.add(user)
        return HttpResponseRedirect('dentistlogin')
    return render(request,'clinic/dentistsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDentistId=request.POST.get('assignedDentistId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'clinic/patientsignup.html',context=mydict)






#-----------for checking user is dentist , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_dentist(user):
    return user.groups.filter(name='Dentist').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,Dentist OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_dentist(request.user):
        accountapproval=models.Dentist.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('dentist-dashboard')
        else:
            return render(request,'clinic/dentist_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'clinic/patient_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    dentists=models.Dentist.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    dentistcount=models.Dentist.objects.all().filter(status=True).count()
    pendingdentistcount=models.Dentist.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'dentists':dentists,
    'patients':patients,
    'dentistcount':dentistcount,
    'pendingdentistcount':pendingdentistcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'clinic/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dentist_view(request):
    return render(request,'clinic/admin_dentist.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_dentist_view(request):
    dentists=models.Dentist.objects.all().filter(status=True)
    return render(request,'clinic/admin_view_dentist.html',{'dentists':dentists})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_dentist_from_clinic_view(request,pk):
    dentist=models.Dentist.objects.get(id=pk)
    user=models.User.objects.get(id=dentist.user_id)
    user.delete()
    dentist.delete()
    return redirect('admin-view-dentist')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_dentist_view(request,pk):
    dentist=models.Dentist.objects.get(id=pk)
    user=models.User.objects.get(id=dentist.user_id)

    userForm=forms.DentistUserForm(instance=user)
    dentistForm=forms.DentistForm(request.FILES,instance=dentist)
    mydict={'userForm':userForm,'dentistForm':dentistForm}
    if request.method=='POST':
        userForm=forms.DentistUserForm(request.POST,instance=user)
        dentistForm=forms.DentistForm(request.POST,request.FILES,instance=dentist)
        if userForm.is_valid() and dentistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            dentist=dentistForm.save(commit=False)
            dentist.status=True
            dentist.save()
            return redirect('admin-view-dentist')
    return render(request,'clinic/admin_update_dentist.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_dentist_view(request):
    userForm=forms.DentistUserForm()
    dentistForm=forms.DentistForm()
    mydict={'userForm':userForm,'dentistForm':dentistForm}
    if request.method=='POST':
        userForm=forms.DentistUserForm(request.POST)
        dentistForm=forms.DentistForm(request.POST, request.FILES)
        if userForm.is_valid() and dentistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            dentist=dentistForm.save(commit=False)
            dentist.user=user
            dentist.status=True
            dentist.save()

            my_dentist_group = Group.objects.get_or_create(name='Dentist')
            my_dentist_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-dentist')
    return render(request,'clinic/admin_add_dentist.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_dentist_view(request):
    #those whose approval are needed
    dentists=models.Dentist.objects.all().filter(status=False)
    return render(request,'clinic/admin_approve_dentist.html',{'dentists':dentists})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_dentist_view(request,pk):
    dentist=models.Dentist.objects.get(id=pk)
    dentist.status=True
    dentist.save()
    return redirect(reverse('admin-approve-dentist'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_dentist_view(request,pk):
    dentist=models.Dentist.objects.get(id=pk)
    user=models.User.objects.get(id=dentist.user_id)
    user.delete()
    dentist.delete()
    return redirect('admin-approve-dentist')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_dentist_specialisation_view(request):
    dentists=models.Dentist.objects.all().filter(status=True)
    return render(request,'clinic/admin_view_dentist_specialisation.html',{'dentists':dentists})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'clinic/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'clinic/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_clinic_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDentistId=request.POST.get('assignedDentistId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'clinic/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDentistId=request.POST.get('assignedDentistId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'clinic/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'clinic/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'clinic/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDentist=models.User.objects.all().filter(id=patient.assignedDentistId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDentistName':assignedDentist[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'dentistFee':request.POST['dentistFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['dentistFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDentistName=assignedDentist[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.dentistFee=int(request.POST['dentistFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['dentistFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'clinic/patient_final_bill.html',context=patientDict)
    return render(request,'clinic/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDentistName':dischargeDetails[0].assignedDentistName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'dentistFee':dischargeDetails[0].dentistFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('clinic/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'clinic/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'clinic/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.dentistId=request.POST.get('dentistId')
            appointment.patientId=request.POST.get('patientId')
            appointment.dentistName=models.User.objects.get(id=request.POST.get('dentistId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'clinic/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'clinic/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ Dentist RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDentistId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,dentistId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDentistName=request.user.first_name).count()

    #for  table in dentist dashboard
    appointments=models.Appointment.objects.all().filter(status=True,dentistId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'dentist':models.Dentist.objects.get(user_id=request.user.id), #for profile picture of dentist in sidebar
    }
    return render(request,'clinic/dentist_dashboard.html',context=mydict)



@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_patient_view(request):
    mydict={
    'dentist':models.Dentist.objects.get(user_id=request.user.id), #for profile picture of dentist in sidebar
    }
    return render(request,'clinic/dentist_patient.html',context=mydict)





@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDentistId=request.user.id)
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    return render(request,'clinic/dentist_view_patient.html',{'patients':patients,'dentist':dentist})


@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def search_view(request):
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDentistId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'clinic/dentist_view_patient.html',{'patients':patients,'dentist':dentist})



@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDentistName=request.user.first_name)
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    return render(request,'clinic/dentist_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'dentist':dentist})



@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_appointment_view(request):
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    return render(request,'clinic/dentist_appointment.html',{'dentist':dentist})



@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_view_appointment_view(request):
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,dentistId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'clinic/dentist_view_appointment.html',{'appointments':appointments,'dentist':dentist})



@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def dentist_delete_appointment_view(request):
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,dentistId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'clinic/dentist_delete_appointment.html',{'appointments':appointments,'dentist':dentist})



@login_required(login_url='dentistlogin')
@user_passes_test(is_dentist)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    dentist=models.Dentist.objects.get(user_id=request.user.id) #for profile picture of dentist in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,dentistId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'clinic/dentist_delete_appointment.html',{'appointments':appointments,'dentist':dentist})



#---------------------------------------------------------------------------------
#------------------------ Dentist RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    dentist=models.Dentist.objects.get(user_id=patient.assignedDentistId)
    mydict={
    'patient':patient,
    'dentistName':dentist.get_name,
    'dentistMobile':dentist.mobile,
    'dentistAddress':dentist.address,
    'symptoms':patient.symptoms,
    'dentistDepartment':dentist.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'clinic/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'clinic/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('dentistId'))
            desc=request.POST.get('description')

            dentist=models.Dentist.objects.get(user_id=request.POST.get('dentistId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.dentistId=request.POST.get('dentistId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.dentistName=models.User.objects.get(id=request.POST.get('dentistId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'clinic/patient_book_appointment.html',context=mydict)



def patient_view_dentist_view(request):
    dentists=models.Dentist.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'clinic/patient_view_dentist.html',{'patient':patient,'dentists':dentists})



def search_dentist_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    dentists=models.Dentist.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'clinic/patient_view_dentist.html',{'patient':patient,'dentists':dentists})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'clinic/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDentistName':dischargeDetails[0].assignedDentistName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'dentistFee':dischargeDetails[0].dentistFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'clinic/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'clinic/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'clinic/contactussuccess.html')
    return render(request, 'clinic/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
