from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormRegistro(UserCreationForm):
    
    # def __init__(self,*args,**kwargs):
    #     super(FormRegistro,self).__init__(*args,**kwargs)
    #     for i in self.visible_fields():
    #         i.field.widget.attrs["class"]="form-control"
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2", "is_superuser", "is_staff", "is_active")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }