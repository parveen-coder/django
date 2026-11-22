import re
from django import forms 

from .models import Car, Student, Cloth






class ExamForm(forms.Form):
      name = forms.CharField(required=True, min_length=3, max_length=20, error_messages={ 'min_length':'Minimum 3 characters required'})
      age = forms.IntegerField(required=False)
      email = forms.EmailField()
     


      


class Newform(forms.Form):
       name=forms.CharField()
       email=forms.EmailField()
       roll=forms.IntegerField()




class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'


class StudentFormNew(forms.ModelForm):
       class Meta: 
            model= Student
            fields = '__all__'


class ClothForm(forms.ModelForm):
       class Meta:
              model=Cloth
              fields = '__all__'








class RegisterStudent(forms.Form):
    name= forms.CharField(required=True, min_length=3, max_length=15,  error_messages={'required': 'Please enter your name.',
            'max_length': 'Name cannot contain more than 15 characters.'})
    email= forms.EmailField(error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email address.'
        })
    age=forms.IntegerField(required=False)
    country=forms.CharField()
    image=forms.ImageField()
    file=forms.FileField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[A-Za-z ]+$',name):
            raise forms.ValidationError(
                "Name should contain only letters and spaces."
            )
        return name
   
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError(
                 "Only Gmail addresses are allowed."
            )
   
        return email
   
    def clean_image(self):
        image = self.cleaned_data['image']

        if image.size > 2 * 1024 * 1024:

            raise forms.ValidationError(
                "Image must be smaller than 2 MB."
            )

        allowed_types = [
            'image/jpeg',
            'image/png'
        ]

        if image.content_type not in allowed_types:

            raise forms.ValidationError(
                "Only JPG and PNG images are allowed."
            )

        return image





class StudentForm(forms.Form):

    name = forms.CharField(required=True, max_length=100)

    email = forms.EmailField(required=True)

    age = forms.IntegerField(required=True, min_value=18, max_value=60)

    image = forms.ImageField()

    file = forms.FileField()





















