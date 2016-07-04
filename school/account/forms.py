from django import forms
from django.contrib.auth.models import User
from account.models import Profile

class UserForm(forms.ModelForm):
    username = forms.CharField(label='帳號')
    username.widget.attrs.update({'class':'form-control'})
    password = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    password.widget.attrs.update({'class':'form-control'})
    password2 = forms.CharField(widget=forms.PasswordInput(), label='確認密碼')
    password2.widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password!=password2:
            raise forms.ValidationError('密碼不相符')
        return password2

class UserProfileForm(forms.ModelForm):
    fullName = forms.CharField(max_length=128, label='姓名')
    fullName.widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = Profile
        fields = ('fullName', )