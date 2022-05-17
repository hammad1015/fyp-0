from django.shortcuts import render, redirect
from django.views     import generic
from django.urls      import reverse_lazy
from django.views.generic.edit import FormView

from django.conf                 import settings
from django.http 		         import HttpResponse
from django.contrib		         import messages
from django.contrib.auth         import login, authenticate, logout
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail            import send_mail
from validate_email import validate_email

import random
import string
import json

from .forms import SignUpForm, SignInForm, AccountVerificationForm
from .models import User, ProcessedEmail


# user resgitration view
class SignUpView(generic.View):
	template_name = 'accounts/signup.html'
	form_class    = SignUpForm

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('profile')

		return render(request, self.template_name, {'form':self.form_class})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			email    = form.cleaned_data['email']
			
			is_valid_email = validate_email(email_address=email)
			if not is_valid_email:
				email_error = 'Please enter a valid email' 
				return render(request, self.template_name, {'form':form, 'email_error':email_error})

			else:
				user = form.save()
				user.is_active = False

				user.code = ''.join(random.sample(string.ascii_letters+string.digits, 6))
				user.save()

				subject        = 'Verify your MailEx account'
				message        = f'Here is your 6-digit verification code: {user.code}'
				email_from     = settings.EMAIL_HOST_USER
				recipient_list = [email]

				send_mail(subject, message, email_from, recipient_list)

				return redirect('account_verification')
		
		else:
			return render(request, self.template_name, {'form':form})


class SignInView(generic.View):
	template_name = 'accounts/signin.html'
	form_class    = SignInForm

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('profile')

		return render(request, self.template_name, {'form':self.form_class})

	def post(self, request):
		form = self.form_class(request, data=request.POST)

		if form.is_valid():
			email    = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			user = authenticate(username=username, password=password)
			if user is not None and user.email == email:
				login(request, user)
				messages.success(request, "You have successfully logged in.")
				return redirect('profile')

			else:
				email_error = 'Please enter a valid email' if user.email != email else None
				return render(request, self.template_name, {'form':form, 'email_error':email_error})

		else:
			return render(request, self.template_name, {'form':form})


class SignOutView(generic.View):

	def get(self, request):
		if request.user is None:
			messages.warning(request, "You are not logged in!")
			return redirect('home')

		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect('home')


class ProfileView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'accounts/profile.html'
	login_url = 'signin'
	redirect_field_name = None

	def get(self, request):
		if request.user is None:
			messages.warning(request, "You are not logged in!")
			return redirect('home')

		return render(request, self.template_name)


class AccountVerification(generic.View):
	template_name = 'accounts/account_verification.html'
	form_class    = AccountVerificationForm

	def get(self, request):
		return render(request, self.template_name,  {'form':self.form_class})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			code = form.cleaned_data.get('verification_code')
			try:
				user = User.objects.get(code=code)
				user.is_active = True

				# set total number of emails
				totalemails = len(ProcessedEmail.objects.filter(from_user={'address': request.user.email}))
				user.emails = totalemails if totalemails is not None else 0
				user.save()
				return redirect('signin')

			except Exception as DoesNotExist:
				invalid_code = 'Please enter a valid code' 
				return render(request, self.template_name, {'form':self.form_class, 'msg':invalid_code})
				

def download_all_emails(request):

	if not request.user.is_authenticated:
		messages.warning(request, "You are not logged in!")
		return redirect('home')

	processed_emails = ProcessedEmail.objects.filter(from_user={'address': request.user.email})			

	json_output = []
	for email in processed_emails:
		json_output.append({
			"id"      : email.id,
			"from"    : email.from_user,
			"subject" : email.subject,
			"body"    : email.body,
			"entities": email.entities
			})

	filename = request.user.username + "_emails.json"
	response = HttpResponse(json.dumps({"data":json_output}), content_type='application/json')
	response['Content-Disposition'] = f'attachment; filename={filename}'
	
	request.user.downloads   = request.user.downloads   + len(json_output)
	request.user.totalemails = len(processed_emails) if len(processed_emails) is not None else 0
	
	request.user.save()
	return response

	
def download_latest_emails(request):

	if not request.user.is_authenticated:
		messages.warning(request, "You are not logged in!")
		return redirect('home')

	processed_emails = ProcessedEmail.objects.filter(from_user={'address': request.user.email})		

	totalemails      = len(processed_emails)	
	latest_emails    = totalemails - request.user.downloads

	json_output = []
	for email in processed_emails[-latest_emails:]:
		json_output.append({
			"id"      : email.id,
			"from"    : email.from_user,
			"subject" : email.subject,
			"body"    : email.body,
			"entities": email.entities
			})

	filename = request.user.username + "_emails.json"
	response = HttpResponse(json.dumps({"data":json_output}), content_type='application/json')
	response['Content-Disposition'] = f'attachment; filename={filename}'
	
	request.user.downloads   = request.user.downloads   + len(json_output)
	request.user.totalemails = len(processed_emails) if len(processed_emails) is not None else 0
	
	request.user.save()
	return response
