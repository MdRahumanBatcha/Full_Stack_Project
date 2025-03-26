from rest_framework import serializers
from My_app.models import *

class addProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
class addServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = 'service_name', 'service_description', 'service_image'