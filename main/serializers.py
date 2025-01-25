from rest_framework import serializers
from .models import Skills, JobPost

from organization.serializers import  OrganizationSerializer
from users.serializers import UserSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model= Skills
        fields= ['name']

class JobPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobPost
        fields= ['title', 'job_desc', 'workplace_type', 'location'
                 'job_type', 'skills']

class JobPostSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    organization= OrganizationSerializer()
    skills= SkillSerializer(many=True)
    class Meta:
        model= JobPost
        fields= ['user','organization', 'title', 'job_desc', 'workplace_type',
                 'location', 'job_type', 'skills']
