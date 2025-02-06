from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import JobPostSerializer,JobPostCreateSerializer,ApplicantCreateSerializer
from .models import JobPost,Applicant

# Create your views here.

class JobViewSet(viewsets.ModelViewSet):
    permission_classes= (permissions.IsAuthenticated)
    serializer_class= JobPostSerializer

    def get_queryset(self):
        user= self.request.user
        organization= user.organization_set.first()
        return JobPost.objects.filter(organization=organization)
    
    def create(self, request, *args, **kwargs):
        serializer= JobPostCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, organization= request.user.organization_set.first())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = JobPostCreateSerializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance= self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    

    @action(methods= ("GET"), url_path='applicants')
    def job_applicants(self, request):
        instance= self.get_object()
        applicants= Applicant.objects.filter(job=instance)
        return applicants
    
    @action(methods= ("POST"), url_path='apply')
    def apply_job(self, request):
        instance= self.get_object()
        serializer= ApplicantCreateSerializer(
            data= request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(job= instance)
        return Response({"detail": "Applied"}, status=status.HTTP_201_CREATED)
