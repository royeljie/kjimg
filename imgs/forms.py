from django import forms
from imgs import models


class CertificateForm(forms.ModelForm):
    class Meta:
        model = models.Certificate
        fields = ['sn']


class OrgForm(forms.ModelForm):
    class Meta:
        model = models.Org
        fields = ['id', 'name']


class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['org', 'fullname', 'username', 'is_active', 'role']


# class AccountForm(forms.ModelForm):
#     class Meta:
#         model = models.Account
#         fields = ['id', 'code', 'name']


class RejectInfoForm(forms.ModelForm):
    class Meta:
        model = models.RejectInfo
        fields = ['reason', 'certificate']


class SearchCertificateForm(forms.Form):
    scope = forms.ChoiceField(
        choices=[('todo', 'todo'), ('submitted', 'submitted'), ('belonged', 'belonged'), ('all', 'all'),])
    orgId = forms.IntegerField()
    accountId = forms.IntegerField()
    detail = forms.CharField()
    beginDate = forms.DateField()
    endDate = forms.DateField()


class ParamForm(forms.ModelForm):
    class Meta:
        model = models.Param
        fields = ['id', 'name', 'code', 'val']


