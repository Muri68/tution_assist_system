from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from authentications.views import check_role_university
from authentications.models import User
from .models import University
from students.models import Student, StudentCampaign
from authentications.forms import UserForm
from students.forms import StudentForm, StudentCampaignForm
from donations.models import Donations

from django.db.models import Sum



def get_university(request):
    uni = University.objects.get(user=request.user)
    return uni

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_university)
def UniversityDashboard(request):
    university = get_object_or_404(University, user=request.user)
    all_students = Student.objects.filter(university_id=university)
    university_donations = Donations.objects.filter(verified=True, student_university=university).order_by('-created_at')[:5]
    all_donations = Donations.objects.filter(student_university=university)
    all_campaign = StudentCampaign.objects.filter(student_university=university).order_by('-created_at')
    
        
    total_donation = all_donations.aggregate(Sum('amount'))
    total_amount_needed = all_campaign.aggregate(Sum('financial_need'))
    
    context = {
        'university': university,
        'all_students': all_students,
        'all_donations': all_donations,
        'total_donation' : total_donation,
        'total_amount_needed': total_amount_needed,
        'university_donations': university_donations,
    }
    return render(request, 'university/universityDashboard.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_university)
def universityAddStudent(request):
    university = get_object_or_404(University, user=request.user)
    user_form = UserForm(request.POST)
    student_form = StudentForm(request.POST, request.FILES,)
    if request.method == 'POST':
        if user_form.is_valid() and student_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.user_type = User.STUDENT
            user.is_active = True
            user.save()
            
            
            student = student_form.save(commit=False)
            student.user = user
            student_id = student_form.cleaned_data['student_id']
            full_name = student_form.cleaned_data['full_name']
            profile_picture = student_form.cleaned_data['profile_picture']
            gender = student_form.cleaned_data['gender']
            phone_number = student_form.cleaned_data['phone_number']
            address = student_form.cleaned_data['address']
            
            
            
            student.is_verified = True
            student.university_id = university.id
            student.save()
            context = {
                'user_form': user_form,
                'student_form': student_form,
            }
            
            messages.success(request, 'Account Created successfully!')
            return redirect('universityStudents')
        
        else:
            print('invalid form')
            print(user_form.errors, student_form)
            messages.error(request, user_form.errors)
            
    
    context = {
        'university': university,
        'user_form': user_form,
        'student_form': student_form,
    }
    return render(request, 'university/addStudent.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_university)
def edit_student(request, student_id):
    d_student = get_object_or_404(Student, id=student_id)
    user_form = UserForm(request.POST, instance=d_student.user)
    student_form = StudentForm(request.POST, request.FILES, instance=d_student)
    context = {
        'user_form': user_form,
        'student_form': student_form,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':
        if user_form.is_valid() and student_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            
            try:
                user = User.objects.get(id=student.user.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                
                
                student = student_form.save(commit=False)
                student.user = user
                student_id = student_form.cleaned_data['student_id']
                full_name = student_form.cleaned_data['full_name']
                profile_picture = student_form.cleaned_data['profile_picture']
                gender = student_form.cleaned_data['gender']
                phone_number = student_form.cleaned_data['phone_number']
                address = student_form.cleaned_data['address']
                
                student.is_verified == True
                student.university_id = get_university(request)
                student.save()
                context = {
                    'user_form': user_form,
                    'student_form': student_form,
                }
            
                messages.success(request, 'Account Created successfully!')
                return redirect('universityStudents')
                    
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "university/edit_student.html", context)




# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_university)
def universityAllStudent(request):
    university = get_object_or_404(University, user=request.user)
    all_students = Student.objects.filter(university_id=university).order_by('-student_id')

    
    context = {
        'university': university,
        'all_students': all_students,
    }
    return render(request, 'university/allStudent.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_university)
def universityViewStudent(request, student_id):
    university = get_object_or_404(University, user=request.user)
    student = get_object_or_404 (Student, id=student_id)
    student_campaign = StudentCampaign.objects.filter(user=student).last()

    
    context = {
        'university': university,
        'student': student,
        'student_campaign': student_campaign,
    }
    return render(request, 'university/studentDetail.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_university)
def UniversityAddStudentsCampaign(request, student_id):
    university = get_object_or_404(University, user=request.user)
    student = get_object_or_404 (Student, id=student_id)
    student_campaign = StudentCampaign.objects.filter(user=student)
   
    if request.method == 'POST':
        form = StudentCampaignForm(request.POST, request.FILES)
        if form.is_valid():
            student_credentials = form.cleaned_data['student_credentials']
            financial_need = form.cleaned_data['financial_need']
            campaign_message = form.cleaned_data['campaign_message']
            payment_deadline = form.cleaned_data['payment_deadline']
            campaign = StudentCampaign.objects.create(user=student, student_university=student.university, student_credentials=student_credentials, financial_need=financial_need, campaign_message=campaign_message, payment_deadline=payment_deadline)
            campaign.save()
            messages.success(request, 'Campaign created Successfully.')
            return redirect('universityStudentCampaign')
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = StudentCampaignForm()

    
    context = {
        'university': university,
        'student': student,
        'student_campaign': student_campaign,
        'form': form,
        'campaign': campaign,
    }
    return render(request, 'university/addStudentsCampaign.html', context)





# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_university)
def universityDonations(request):
    university = get_object_or_404(University, user=request.user)
    all_donations = Donations.objects.filter(verified=True, student_university=university).order_by('-created_at')
    
    context = {
        'university': university,
        'all_donations': all_donations,
    }
    return render(request, 'university/donations.html', context)




# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_university)
def UniversityStudentsCampaign(request):
    university = get_object_or_404(University, user=request.user)
    
    all_campaign = StudentCampaign.objects.filter(student_university=university).order_by('-created_at')
    context = {
        'university': university,
        'all_campaign': all_campaign,
    }
    return render(request, 'university/studentsCampaign.html', context)



# @login_required(login_url='login')
# @user_passes_test(check_role_university)
# def UniversityAddStudentsCampaign(request):
#     university = get_object_or_404(University, user=request.user)    
#     all_students = Student.objects.filter(university_id=university)
        
#     context = {
#         'university': university,
#         'all_students': all_students,
#     }
#     if request.method == 'GET':
#         return render(request, 'university/addStudentsCampaign.html', context)
    
#     if request.method == 'POST':
#         user = request.POST.get('user')
#         student_credentials = request.POST.get('student_credentials')
#         financial_need = request.POST.get('financial_need')
#         campaign_message = request.POST.get('campaign_message')
#         payment_deadline = request.POST.get('payment_deadline')

#         if not user:
#             messages.error(request, 'Student is required')
#             return render(request, 'university/addStudentsCampaign.html', context)

#         StudentCampaign.objects.create(user=user, student_university=university.id, 
#                 student_credentials=student_credentials, financial_need=financial_need, 
#                 campaign_message=campaign_message, payment_deadline=payment_deadline)
#         # campaign.save(commit=False)
#         # campaign.is_approve = True
        
#         messages.success(request, 'Student Campaign saved successfully')

#         return redirect('universityStudentCampaign')

