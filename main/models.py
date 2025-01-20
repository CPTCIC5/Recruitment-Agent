from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

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

class Skills(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class JobPost(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    organization= models.ForeignKey(Organization, on_delete= models.CASCADE)

    title= models.CharField(max_length=100)
    job_desc= models.TextField()
    workplace_type= models.IntegerField(choices=WORKPLACE_TYPES)
    location= models.CharField(max_length=100)
    job_type= models.IntegerField(choices=WORK_TYPES)
    skills= models.ManyToManyField(Skills)


    created_at= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
