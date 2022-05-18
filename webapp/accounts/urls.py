from django.urls import path

from .views import *

urlpatterns = [
	path(''        , generic.TemplateView.as_view(template_name='accounts/index.html'), name='home'),
	path('signup'  , SignUpView.as_view(), name='signup'),
	path('signin'  , SignInView.as_view(), name='signin'),
	path('signout' , SignOutView.as_view(), name='signout'),
	path('help'    , generic.TemplateView.as_view(template_name='accounts/help.html'), name='help'),
	path('profile' , ProfileView.as_view(), name='profile'),
	path('download_all', download_all_emails, name='download_all'),
	path('download_latest', download_latest_emails, name='download_latest'),
	path('email_preview', email_preview, name="email_preview"),
	path('account_verification',AccountVerification.as_view(), name='account_verification'),
]