import fitz  # PyMuPDF
from django.db import models
from users.models import User
from organization.models import Organization
from openai import OpenAI
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from dotenv import load_dotenv

load_dotenv()
client= OpenAI()

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

class Applicant(models.Model):
    job= models.ForeignKey(JobPost, on_delete=models.CASCADE)
    resume= models.FileField(upload_to='Candidates-Resume', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])


    def __str__(self):
        return str(self.job)


    def pdf_to_text(self, pdf_path):
        document = fitz.open(pdf_path)
        text = []
        
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            
            blocks = page.get_text("blocks")  
            page_text = " ".join(block[4] for block in sorted(blocks, key=lambda b: (b[1], b[0])))
            
            text.append(page_text.strip())

        final_text = "\n\n".join(text)
        print(final_text)
        return final_text

    def create_vector_embeddings(self, text):
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embeddings = response.data[0].embedding
        return embeddings
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        pdf_path= self.resume.path
        try:
            text= self.pdf_to_text(pdf_path)
            embeddings= self.create_vector_embeddings(text)
            # Save or use the embeddings as needed
            print("Vector Embeddings:", embeddings)
        except Exception as e:
            raise ValidationError(f"Error processing resume: {e}")