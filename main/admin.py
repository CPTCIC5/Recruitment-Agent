from django.contrib import admin
from .models import JobPost, Candidate


admin.site.register(Candidate)
admin.site.register(JobPost)

#admin.site.register()