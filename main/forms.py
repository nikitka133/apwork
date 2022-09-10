from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import PasswordInput, ModelForm
from phonenumber_field.formfields import PhoneNumberField
from main.models import ROLE, Job, Proposal
from main.models import AdvUser


class UserCrForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input', "placeholder": "Логин"}))
    password1 = forms.CharField(label='', widget=PasswordInput(attrs={"placeholder": "Пароль"}))
    password2 = forms.CharField(label='', widget=PasswordInput(attrs={"placeholder": "Повторите пароль"}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         "placeholder": "Имя"}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                        "placeholder": "Фамилия"}))
    phone = PhoneNumberField(label='', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                     "placeholder": "Телефон", 'value': '+7'}))
    role = forms.ChoiceField(choices=ROLE, label="")
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-input', "placeholder": "Email"}))

    class Meta:
        model = AdvUser
        fields = ('role', 'username', 'first_name', 'last_name', 'email', 'phone',)


class CreateJobForm(ModelForm):
    expired_date = forms.DateField(help_text='Необходимо завершить до', widget=forms.DateInput({'type': 'date'}))

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('is_active', 'processing', 'offer', 'executor')
        widgets = {'author': forms.HiddenInput}


class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = 'first_name', 'last_name',


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.TextInput(attrs={'type': 'password'}))
    new_password2 = forms.CharField(label='Повтрите новый пароль', widget=forms.TextInput(attrs={'type': 'password'}))


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = '__all__'
        exclude = ('accepted',)
        widgets = {'sender': forms.HiddenInput,
                   'employer': forms.HiddenInput,
                   'job': forms.HiddenInput,
                   }


class ChangeJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('is_active', 'processing', 'offer', 'executor')
        widgets = {'author': forms.HiddenInput}
