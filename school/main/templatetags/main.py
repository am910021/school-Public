from django import template
from main.models import Menu, Item, ShinyApp


register = template.Library()

@register.filter(name='getItemQty')
def getItemQty(menu):
    return len(Item.objects.filter(menu=menu))


@register.filter(name='getItem')
def getItem(menu):
    return Item.objects.filter(menu=menu)


@register.filter(name='delOneNumber')
def delOneNumber(data):
    data.pop(0)
    return ""

@register.filter(name='getNumber')
def getNumber(data):
    return data[0]+1

@register.filter(name='setHide')
def setHide(data):
    num=data[0]+1
    style="""
    display:none
    """
    style2="""
    display:black
    """
    print(num)
    return style2 if num==1 else style


@register.filter(name='setClass')
def setClass(data):
    value = data[0]
    return "active" if value % 2==0 else "info"


@register.filter(name='nextRow')
def nextRow(data):
    num=data+1
    html="""
        </div>
    <div class="row" style="margin-top:5px">
    """
    return html if num%4==0 else ""

@register.filter(name='plus')
def plus(data):
    return data+1

@register.filter(name='getName')
def getName(id, data):
    return data[id].name

@register.filter(name='isEqual')
def isEqual(id1, id2):
    return True if str(id1)==str(id2) else False

@register.filter(name='isOpen')
def isOpen(id1, id2):
    style="""
    class=open
    """
    return style if str(id1)==str(id2) else ""

@register.filter(name='isHide')
def isHide(id1, id2):
    style="""
    style=display:block;
    """
    return style if str(id1)==str(id2) else ""


