from django.contrib import admin
from .models import JobPost,Question, Candidate, CandidateResponse,JobPostQuestion
# Register your models here.
admin.site.register(Candidate)
admin.site.register(JobPost)
admin.site.register(Question)
admin.site.register(JobPostQuestion)
admin.site.register(CandidateResponse)
#admin.site.register()