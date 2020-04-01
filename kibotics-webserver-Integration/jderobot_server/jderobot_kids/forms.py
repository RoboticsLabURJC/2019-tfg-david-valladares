# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Code, Exercise, CodePermissions
from django.contrib.admin.widgets import FilteredSelectMultiple

User = get_user_model()

class UserForm(UserCreationForm):
    username = forms.CharField(min_length=6, max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=60, required=True)
    code = forms.CharField(max_length=16, required=True)
    password1 = forms.CharField(min_length=8, max_length=16, required=True)
    password2 = forms.CharField(min_length=8, max_length=16, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'code', 'password1', 'password2')

    def clean_code(self):
        code = self.cleaned_data['code']
        if code != "" and not Code.objects.filter(code=code).exists():
            raise forms.ValidationError("El código introducido no es válido")
        return code

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username[-1].isalnum():
            raise forms.ValidationError("El nombre de usuario debe terminar con un número o una letra [0-9a-zA-Z]")
        return username

class CodesGeneratorForm(ModelForm):
    
    num_codes = forms.IntegerField(label="Número de códigos", min_value=1)
    expiration = forms.DateField(label="Finalización del Periodo de Suscripción", 
                                 required=True,
                                 widget=forms.SelectDateWidget()
    )
    packs = forms.ModelMultipleChoiceField(
        queryset=Exercise.tags.all(),
        required=False,
        widget = forms.CheckboxSelectMultiple(attrs={'class': 'multiple'}),
        label='Selecciona los Packs de Ejercicios',
    )

    class Meta:
        model = Code
        fields = ('num_codes', 'group', 'packs', 'exercises', 'promotional', 'observations')

class IndividualPermissionsForm(ModelForm):
    
    packs = forms.ModelMultipleChoiceField(
        queryset=Exercise.tags.all(),
        required=False,
        widget=FilteredSelectMultiple("Packs", False),
        label='Selecciona los Packs de Ejercicios sobre los que quieras aplicar los permisos',
    )
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Ejercicios", False),
        label='Selecciona los Ejercicios sobre los que quieras aplicar los permisos',
    )

    class Meta:
        model = CodePermissions
        fields = ('user', 'p', 'r', 'w', 'x')

class GroupPermissionsForm(ModelForm):
    
    group = forms.ModelChoiceField(
        queryset=User.group.all(),
        required=True,
        label='Selecciona el Grupo al que quieras asignar Permisos',
    )
    packs = forms.ModelMultipleChoiceField(
        queryset=Exercise.tags.all(),
        required=False,
        widget=FilteredSelectMultiple("Packs", False),
        label='Selecciona los Packs de Ejercicios sobre los que quieras aplicar los permisos',
    )
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Ejercicios", False),
        label='Selecciona los Ejercicios sobre los que quieras aplicar los permisos',
    )

    class Meta:
        model = CodePermissions
        fields = ('group', 'p', 'r', 'w', 'x')

class GroupCreationForm(ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre del Grupo"
        })
    )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=FilteredSelectMultiple("Usuarios", False),
        label='Selecciona los miembros del Grupo',
    )

    class Meta:
        model = User
        fields = ('name', 'members')

class PackCreationForm(ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre del Pack"
        })
    )
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        required=True,
        widget=FilteredSelectMultiple("Ejercicios", False),
        label='Selecciona los Ejercicios que conformarán el Pack',
    )

    class Meta:
        model = Exercise
        fields = ('name', 'exercises')

class CodePacksForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(CodePacksForm, self).__init__(*args, **kwargs)
        options = Exercise.tags.all()
        w = self.fields['packs'].widget
        choices = []
        for choice in options:
            choices.append((choice.id, choice.name))
        w.choices = choices

