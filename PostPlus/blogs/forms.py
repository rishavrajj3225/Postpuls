from django import forms
from .models import blog
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class blogForm(forms.ModelForm):
    class Meta:
        model= blog
        fields= ['title','summary','content','image','tags']
        widgets= {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }
class UserRegistrationForm(UserCreationForm):
    email= forms.EmailField(required=False)
    class Meta:
        model= User
        fields= ('username','email','password1','password2')
        #jab v hum builtin form use karte hain toh hume uske fields ko define karna padta hai tuple me and agar khud se banate hai to array pass krna hota hai
    