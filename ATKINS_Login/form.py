from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    email_error_messages = {'required': '--- The E-mail is required ---'}
    password_error_messages = {'required': '--- The Password is required ---'}
    name_error_messages = {'required': '--- The Name is required ---'}

    first_name = forms.CharField(error_messages=name_error_messages, label='Name')
    username = forms.EmailField(error_messages=email_error_messages, label='E-mail address')

    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password', error_messages=password_error_messages)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password',
                                error_messages=password_error_messages)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("--- Passwords don't match ---")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)

        # Hash the password with the set_password method.
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
