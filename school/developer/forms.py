from django import forms
from db.models import Demo

class DemoForm(forms.ModelForm):
    name = forms.CharField(label='圖表名稱')
    name.widget.attrs.update({'class':'form-control'})
    dirName = forms.CharField(label='資料夾')
    dirName.widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = Demo
        fields = ('name', 'dirName')