from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comments

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email','username':'Username'}

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            
        }

#post form
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description','pic','tags']

#Comment form
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']