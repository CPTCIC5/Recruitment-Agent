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
    questions = models.ManyToManyField("Question", through="JobPostQuestion", related_name="jobs")


    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = (
        ("text", "Text"),
        ("mcq", "Multiple Choice"),
        ("file", "File Upload"),
    )
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default="text")

    def __str__(self):
        return self.text


class JobPostQuestion(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)  # Ordering of questions in a job

    class Meta:
        unique_together = ("job_post", "question")
        ordering = ["order"]  # Default ordering by sequence

    def __str__(self):
        return f"{self.job_post.title} - {self.question.text} ({self.order})"

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
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    email= models.EmailField(("email address"))
    linkedin= models.URLField()
    job= models.ForeignKey(JobPost, on_delete=models.CASCADE)
    stage= models.IntegerField(choices= STAGE)
    resume= models.FileField(upload_to='Candidates-Resume', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])


    class Meta:
        unique_together= ['email', 'linkedin', 'job']


class CandidateResponse(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)  # For text responses
    response_file = models.FileField(upload_to="Responses/", blank=True, null=True)  # For file uploads

    class Meta:
        unique_together = ("candidate", "question")

    def __str__(self):
        return f"{self.candidate.first_name} - {self.question.text}"