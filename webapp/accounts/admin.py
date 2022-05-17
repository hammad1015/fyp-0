from django.contrib import admin
from .models import *

admin.site.register(User)
# admin.site.register(Label)
# admin.site.register(EmailSender)
# admin.site.register(Entity)
admin.site.register(ProcessedEmail)