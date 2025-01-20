from django.db import models

INDUSTRIES= (
    (1, "IT SERVICES"),
    (2, "Product Based"),
    (3, "Finance"),
    (4, "Sport")
)
# Create your models here.
class Organization(models.Model):
    name= models.CharField(max_length=100)
    industry= models.IntegerField(max_length=100, choices=INDUSTRIES)
    url= models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    knowledge= models.JSONField(blank=True, null=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name