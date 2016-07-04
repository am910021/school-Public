from django import forms
from django.contrib.auth.models import User
from account.models import Profile
from main.models import Menu, Item, ShinyApp


class FMenu(forms.ModelForm):
    name = forms.CharField(max_length=128)
    name.widget.attrs.update({'class':'form-control'})
    #isActive = forms.BooleanField(required=False)
    #isActive.initial=True
    
    class Meta:
        model = Menu
        fields = ('name',)
        
        
class FItem(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        assign = kwargs.pop('menu') if 'menu' in kwargs else None
        super(FItem, self).__init__(*args, **kwargs)
        if not assign:
            self.fields['menu'] = forms.ModelChoiceField(queryset=Menu.objects.all())
        else:
            self.fields['menu'] = forms.ModelChoiceField(queryset=Menu.objects.all())
            self.fields['menu'].initial = Menu.objects.get(id=assign)
        self.fields['menu'].widget.attrs.update({'class':'form-control'})
        
    name = forms.CharField(max_length=128)
    name.widget.attrs.update({'class':'form-control'})
    #isActive = forms.BooleanField(required=False)
    #isActive.initial=True
    class Meta:
        model = Item
        fields = ('name',)

    
class FShinyApp(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        assign = kwargs.pop('item') if 'item' in kwargs else None
        super(FShinyApp, self).__init__(*args, **kwargs)
        if not assign:
            self.fields['item'] = forms.ModelChoiceField(queryset=Item.objects.all())
        else:
            self.fields['item'] = forms.ModelChoiceField(queryset=Item.objects.all())
            self.fields['item'].initial = Item.objects.get(id=assign)
        self.fields['item'].widget.attrs.update({'class':'form-control'})
        
    name = forms.CharField(max_length=32)
    name.widget.attrs.update({'class':'form-control'})
    dirName = forms.CharField(max_length=32)
    dirName.widget.attrs.update({'class':'form-control'})
    isActive = forms.BooleanField(required=False)
    isActive.initial=True
    class Meta:
        model = ShinyApp
        fields = ('item', 'name', 'dirName', 'isActive')
        

class UserForm(forms.ModelForm):
    username = forms.CharField(label='帳號')
    username.widget.attrs.update({'class':'form-control'})
    password = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    password.widget.attrs.update({'class':'form-control'})
    password2 = forms.CharField(widget=forms.PasswordInput(), label='確認密碼')
    password2.widget.attrs.update({'class':'form-control'})
    email = forms.EmailField(label='電子郵件')
    email.widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password!=password2:
            raise forms.ValidationError('密碼不相符')
        return password2
    
class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='帳號')
    username.widget.attrs.update({'class':'form-control'})
    password = forms.CharField(widget=forms.PasswordInput(), label='密碼', required=False)
    password.widget.attrs.update({'class':'form-control'})
    password2 = forms.CharField(widget=forms.PasswordInput(), label='確認密碼', required=False)
    password2.widget.attrs.update({'class':'form-control'})
    email = forms.EmailField(label='電子郵件')
    email.widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password!=password2:
            raise forms.ValidationError('密碼不相符。')
        return password2

class UserProfileForm(forms.ModelForm):
    fullName = forms.CharField(max_length=128, label='姓名')
    fullName.widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = Profile
        fields = ('fullName', )