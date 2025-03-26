from django.db import models

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    client_contact = models.CharField(max_length=20, default='+91')
    client_mail = models.EmailField(max_length=50, default='@gmail.com')
    project_location = models.CharField(max_length=30)
    project_description = models.TextField(max_length=60, default='N/A')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=[ 
         ('active', 'Active'), #In Progress
         ('pending', 'Pending'),
         ('not_started', 'Not Started'),
         ('completed', 'Completed')
     ], default='active')
    starting_date = models.DateField(null=True,blank = True)
    ending_date = models.DateField(null=True,blank = True)
    
    def __str__(self):
        return self.project_name 

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_description = models.TextField()
    service_image = models.ImageField(upload_to='static/img/', blank = True, null = True)
    
    def __str__(self):
        return self.service_name
    
class Inquiry(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_contact = models.CharField(max_length=20)
    message = models.TextField()
    inquiry_status = models.CharField(max_length=100, choices=[
         ('all', 'All'),
         ('new', 'New'), 
         ('pending', 'Pending'),
         ('resolved', 'Resolved'),
     ])
    received_date = models.DateField(null=True,blank = True)
    
    def __str__(self):
        return f"Inquiry from {self.sender_name}"
    
class Document(models.Model):
    document_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    document_file = models.FileField(upload_to='static/docs/')
    
    def __str__(self):
        return f"Document for {self.document_name}"