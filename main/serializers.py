from rest_framework import serializers
from .models import JobPost,Applicant

from organization.serializers import  OrganizationSerializer
from users.serializers import UserSerializer

class JobPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobPost
        fields= ['title', 'job_desc', 'workplace_type', 'location'
                 'job_type']

class JobPostSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    organization= OrganizationSerializer()
    class Meta:
        model= JobPost
        fields= ['user','organization', 'title', 'job_desc', 'workplace_type',
                 'location', 'job_type']


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Applicant
        fields= ['resume']

class ApplicantSerializer(serializers.ModelSerializer):
    job= JobPostSerializer()
    class Meta:
        model= Applicant
        fields= ['job', 'resume']