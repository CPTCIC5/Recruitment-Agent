from django.db import models
from users.models import User
from organization.models import Organization
from django.core.validators import FileExtensionValidator

WORKPLACE_TYPES= (
    (1, 'Hybrid'),
    (2, 'On-Site'),
    (3, 'Remote')
)

WORK_TYPES= (
    (1, 'Full-time'),
    (2, 'Part-time'),
    (3, 'Contract'),
    (4, 'Temperory'),
    (5, 'Other'),
    (6, 'Volunteer'),
    (7, 'Internship')
)


# Create your models here.
class JobPost(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    organization= models.ForeignKey(Organization, on_delete= models.CASCADE)

    title= models.CharField(max_length=100)
    job_desc= models.TextField()
    workplace_type= models.IntegerField(choices=WORKPLACE_TYPES)
    location= models.CharField(max_length=100)
    job_type= models.IntegerField(choices=WORK_TYPES)

    portal_link= models.URLField()

    created_at= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


STAGE= (
    (1, "New Lead"),
    (2, "Contacted"),
    (3, "Responded"),
    (4, "Applied"),
    (5, "Recruiter screen"),
    (6, "Second interview"),
    (7, "Onsite"),
    (8, "Offer")
)

class Candidate(models.Model):
    job= models.ForeignKey(JobPost, on_delete=models.CASCADE)
    stage= models.IntegerField(choices= STAGE)
    resume= models.FileField(upload_to='Candidates-Resume', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])