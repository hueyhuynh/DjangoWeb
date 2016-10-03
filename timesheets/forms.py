import re
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from models import Timesheet

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


# Create form class for the Registration form
class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))

    # password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label="Confirm Password")
    # PasswordInput and
    # set an appropriate
    # label

    # clean_<fieldname> method in a form class is used to do custom validation
    # for the field.
    # We are doing a custom validation for the 'password2' field and raising
    # a validation error if the password and its confirmation do not match
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    #def clean_email(self):
    #    try:
    #        user = User.objects.get(email__iexact=self.cleaned_data['email'])
    #    except User.DoesNotExist:
    #        return self.cleaned_data['email']
    #    raise forms.ValidationError(_("The email already exists. Please try another one."))


class PasswordChangeForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    # token = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Token"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                               label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label="Confirm Password")

    # PasswordInput and
    # set an appropriate
    # label

    # clean_<fieldname> method in a form class is used to do custom validation
    # for the field.
    # We are doing a custom validation for the 'password2' field and raising
    # a validation error if the password and its confirmation do not match
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            raise forms.ValidationError(_("The username does not exists. Please try another one."))
        return self.cleaned_data['username']

        # def clean_token(self):
        #    try:
        #        user = User.objects.get(username__iexact=self.cleaned_data['username'], password=self.cleaned_data['token'])
        #    except User.DoesNotExist:
        #       raise forms.ValidationError(_("Either username does not exists or token is wrong."))

    # return self.cleaned_data['token']

    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError(_("The email does not exists. Please try another one."))
        return self.cleaned_data['email']

class CreateTimesheetForm(ModelForm):
    class Meta:
        model = Timesheet
        fields = '__all__'