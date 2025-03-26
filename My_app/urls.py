# from django.contrib import admin
from django.urls import path
from .views import * # importing views from My_app

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', admin_login, name='login'),
    path('logout', admin_logout, name='logut'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('projects/', project_list, name='projects'),
    path('add_project/', add_project, name='add_project'),
    path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('services/', service_list, name='services'),
    path('add_service/', add_service, name='add_service'),
    path('documents/', document_list, name='documents'),
    path('delete_document/<int:document_id>', delete_document, name='delete_document'),
    path('reports/<int:project_id>',  reports, name='reports'),
    path('report/', report, name ='report' ),
    # URLs for API Views
    #Projects -- API
    path('roles/', get_project, name='roles'),
    path('roles_create/', post_project, name='roles_create'),
    path('roles_delete/<int:pk>', drop_project, name='roles_delete'),
    path('roles_update/<int:pk>', put_project, name='roles_update'),
    path('roles_retrieve/<int:pk>', update_project, name='role_retrieve'),
    #Services -- API
    path('get_service/', get_service, name='get_service'),
    path('post_service/', post_service, name='post_service'),
    path('put_service/<int:pk>', put_service, name='put_service'),   
    path('update_service/<int:pk>', update_service, name='update_service'), 
] 