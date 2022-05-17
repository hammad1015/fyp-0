from django                     import forms
from django.contrib.auth.forms  import UserCreationForm, AuthenticationForm
from django.core.exceptions     import ValidationError
from .models                    import User

from validate_email import validate_email


class SignUpForm(UserCreationForm):

	class Meta:
		model  = User 
		fields = ('username', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user  = super(SignUpForm, self).save(commit=False)

		if commit:
			user.save()
			
		return user


class SignInForm(AuthenticationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

	field_order = ['username', 'email', 'password']


class AccountVerificationForm(forms.Form):
	verification_code = forms.CharField(min_length=6, max_length=6, required=True)
