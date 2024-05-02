from django import forms
from .models import Student, StudentCampaign
from authentications.validators import allow_only_images_validator
from university.models import University


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'university', 'profile_picture', 'gender', 'phone_number', 'address']
    
    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'profile_picture', 'gender', 'phone_number', 'address']
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class StudentCampaignForm(forms.ModelForm):
    student_credentials = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = StudentCampaign
        fields = ['student_credentials', 'financial_need', 'campaign_message', 'payment_deadline']
    
    def __init__(self, *args, **kwargs):
        super(StudentCampaignForm, self).__init__(*args, **kwargs)
        
        self.fields['financial_need'].widget.attrs['placeholder'] = 'Amount Needed'
        self.fields['payment_deadline'].widget.attrs['placeholder'] = 'Deadline Date'
        
        

class AmountRaisedForm(forms.ModelForm):
    class Meta:
        model = StudentCampaign
        fields = ['amount_raised',]
