from django import forms
from main.models import Menu, Item, ShinyApp


class FMenu(forms.ModelForm):
    name = forms.CharField(max_length=128)
    name.widget.attrs.update({'class':'form-control'})
    permission = forms.IntegerField()
    permission.widget.attrs.update({'class':'form-control'})
    permission.initial=0
    isActive = forms.BooleanField(required=False)
    isActive.initial=True
    
    class Meta:
        model = Menu
        fields = ('name', 'permission', 'isActive')
        
        
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
    permission = forms.IntegerField()
    permission.widget.attrs.update({'class':'form-control'})
    permission.initial=0
    isActive = forms.BooleanField(required=False)
    isActive.initial=True
    class Meta:
        model = Item
        fields = ('name', 'permission', 'isActive')

    
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
    #permission.initial=1
    isActive = forms.BooleanField(required=False)
    isActive.initial=True
    class Meta:
        model = ShinyApp
        fields = ('item', 'name', 'dirName', 'isActive')