from django.contrib import admin
from .models import JobPost,Question, Candidate
admin.site.register(Candidate)
admin.site.register(JobPost)
admin.site.register(Question)

#admin.site.register()