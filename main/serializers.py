from rest_framework import serializers
from .models import JobPost

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
