from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Service, Document #Inquiry,
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


# Create your views here.
    # view for admin login
def admin_login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('/admin_panel/')
        else:
            messages.error(request, 'Invalid Credentials')
    
    return render(request, 'LoginPage.html')

    # view for admin logout
def admin_logout(request):
    return render(request, 'LoginPage.html')

    # view for admin panel
@login_required(login_url = '/login/') 
def admin_panel(request):
    breadCrumb = {'val' : 'Dashboard'}
    total_project = Project.objects.count()
    cards = [ {'card_name' : 'View Projects', 'description' : total_project, 'icon' : '<i class = "bi bi-clipboard-data" style = "position:relative;right:25px;font-size: 60px;"></i>'},
             {'card_name' : 'Total Clients', 'description' : total_project, 'icon': '<i class = "bi bi-question-circle" style = "position:relative;right:25px;font-size: 60px;"></i>'},
             {'card_name' : 'View Services', 'description' : 'Services Provided', 'icon' : '<i class = "bi bi-tools" style = "position:relative;right:25px;font-size: 60px;"></i>'},
             {'card_name' : 'Reports', 'description' : 'Inspect each project in Detail', 'icon': '<i class = "bi bi-bar-chart" style = "position:relative;right:25px;font-size: 60px;"></i>'},
            ]
    #context = we can also use another variable and store previous variables inside it, and use it inside of return(). dictionary format!!
    return render(request, 'admin_panel.html', { 'breadcrumb': breadCrumb, 'cards': cards })

    # view for listing all projects
def project_list(request):
    breadCrumb = 'Projects'
    project_datas = Project.objects.all()
    return render(request, 'projects.html', {'breadcrumb' : breadCrumb, 'project_datas' : project_datas})

    # view for adding new project
def add_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        client_name = request.POST.get('client_name')
        client_contact = request.POST.get('client_contact')
        client_mail = request.POST.get('client_mail')
        project_description = request.POST.get('project_description')
        project_location = request.POST.get('project_location')
        budget = request.POST.get('budget')
        status = request.POST.get('status')
        starting_date = request.POST.get('starting_date')
        ending_date = request.POST.get('ending_date')
        
        data = Project.objects.create(project_name = project_name, client_name = client_name, client_contact = client_contact, client_mail = client_mail, project_description = project_description, project_location = project_location, budget = budget, status = status, starting_date = starting_date, ending_date = ending_date)
        data.save()
        messages.success(request, 'Project added successfully.')
        return redirect ('/projects/')
    
    return render(request, 'add_project.html')

    # view for project deletion
def delete_project(request, project_id):
    project = Project.objects.get(id = project_id)
    project.delete()
    messages.success(request, 'Record deleted successfully.')
    return redirect('/projects/')

    # view for listing all services
def service_list(request):
    var_services = Service.objects.all()
    breadCrumb = 'Services'
    service_cards = [ {'images' : service.service_image.url,
                       'title' : service.service_name,
                       'time' : 'Last updated 3 mins ago',
                       'description' : service.service_description} 
                     for service in var_services
                    ]
    context = {'breadcrumb' : breadCrumb, 'services' : var_services, 'service_cards' : service_cards}
    # if class.. to display no services were added by Admin
    return render(request, 'services.html', context) 

    # view for adding new service
def add_service(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('service_description')
        service_image  = request.FILES.get('service_image')
        data = Service.objects.create(service_name = service_name, service_description = service_description, service_image = service_image)
        data.save()
        messages.success(request, 'Service added successfully.')
        return redirect('services')
        
    return render(request, 'add_service.html')

    # view for listing all inquiries
# def inquiry_list(request):
#     breadCrumb = 'Inquiries'
    # inquiries = Inquiry.objects.all()
   # return render(request, 'inquiries.html', {'breadcrumb': breadCrumb}) #, {'inquiries': inquiries}

    #view for document list
def document_list(request):
    breadCrumb = {'val' : 'Documents'}
    documents = Document.objects.all()
    if request.method == 'POST':
        document_name = request.POST.get('documentName')
        project_name = request.POST.get('projectName')
        doc_file = request.FILES.get('documentFile')
        try:
            project = Project.objects.get(project_name = project_name)
            data = Document.objects.create(document_name = document_name, project = project, document_file = doc_file)
            data.save()
            messages.success(request, 'Document added successfully.')
        except Project.DoesNotExist:
            messages.error(request, f"Project with name {project_name} does not exist!")
        return redirect('/documents/')
        
    return render(request, 'documents.html', {'breadcrumb': breadCrumb, 'documents': documents}) 

    # view for document deletion
def delete_document(request, document_id):
    document = Document.objects.get(id = document_id)
    document.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('/documents/')

    # view for reports
def reports(request, project_id):
    projects = Project.objects.get(id = project_id)
    breadCrumb = { 'val' : 'Reports'}
    return render(request, 'reports.html', {'breadcrumb': breadCrumb, 'project' : projects})

def report(request):
    return render(request, 'reports.html')


    # API Views for Projects

@api_view(['GET'])
def get_project(request):
  data = Project.objects.all()
  serializer = addProjectSerializer(data, many=True) #many=True because we can fetch many data
  return Response(serializer.data)

@api_view(['POST'])
def post_project(request):
    serializer = addProjectSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Data":serializer.data})
    else:
        return Response({"Data":serializer.errors})

@api_view(['DELETE'])
def drop_project(request,pk):
    data=Project.objects.get(id = pk)
    data.delete()
    return Response("Data Deleted Successfully!")

@api_view(['GET'])
def put_project(request,pk):
  data=Project.objects.get(id=pk)
  serializer = addProjectSerializer(data, many = False) #many=False because we can fetch specific data
  return Response(serializer.data)

@api_view(['POST']) # Alternate for PUT
def update_project(request,pk):
    data=Project.objects.get(id=pk)
    serializer = addProjectSerializer(instance=data,data =request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Data":serializer.data})
    else:
        return Response({"Data":serializer.errors})
    

    #API Views for Services
@api_view(['GET'])
def get_service(response):
    data = Service.objects.all()
    serializer = addServiceSerializer(data, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def post_service(request):
    serializer = addServiceSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Data":serializer.data})
    else:
        return Response({"Data":serializer.errors})

@api_view(['GET'])
def put_service(request,pk):
    try:
        data = Service.objects.get(id = pk)
        serializer = addServiceSerializer(data, many = False) #many=False because we can fetch specific data
        return Response(serializer.data)
    except Service.DoesNotExist:
        return Response({"error": f"Service with id {pk} does not exist!"})

@api_view(['POST']) # Alternate for PUT
def update_service(request,pk):
    data = Service.objects.get(id = pk)
    serializer = addServiceSerializer(instance = data,data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Data":serializer.data})
    else:
        return Response({"Data":serializer.errors})