import re
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from timesheets.models import Timesheet
from django.forms import ModelForm

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

class TimesheetForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    #class Meta:
     #   model = Timesheet
     #   fields = ['total_hours_break', 'submission_date','approval_date','employee','approving_manager']

    #total_hours_worked = forms.IntegerField(widget=forms.NumberInput(attrs=dict(required=True, max_value=24)))
    #total_hours_break = forms.IntegerField(widget=forms.NumberInput(attrs=dict(required=True, max_value=24)))
    #submission_date = forms.DateField(widget=forms.DateInput(attrs=dict(required=True)))
    #approval_date = forms.DateField(widget=forms.DateInput(attrs=dict(required=True)))
