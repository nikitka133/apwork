from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.forms import PasswordInput, ModelForm
from phonenumber_field.formfields import PhoneNumberField
from main.models import ROLE, Job
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
    expired_date = forms.DateField(label='Сделать до', widget=forms.DateInput({'type': 'date'}))

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('is_active', 'processing', 'offer')
        widgets = {'author': forms.HiddenInput}


class ChangeUserInfoForm(forms.ModelForm):
    # email = forms.EmailField(required=True, label="Email!!!")

    class Meta:
        model = AdvUser
        fields = 'first_name', 'last_name', 'email',


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()
