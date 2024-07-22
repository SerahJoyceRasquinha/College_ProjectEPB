
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.login_view, name='login'),
    path('signout/', views.logout_view, name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('get_batch_names/', views.get_batch_names, name='get_batch_names'),
    path('get_subject_names/', views.get_subject_names, name='get_subject_names'),
    path('report/', views.filtered_report, name='report'),
]
