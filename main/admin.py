from django.contrib import admin
from .models import JobPost, Applicant


admin.site.register(Applicant)
admin.site.register(JobPost)

#admin.site.register()