from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='home'),
    path('filter/', views.filters, name='filter'),
    path('chat/', views.chat, name='chat'),
    path('job/', views.JobListView.as_view(), name='job'),
    path('job/<int:pk>', views.job_view, name='job_view'),
    path('job/category/<slug:slug_sub_cat>', views.JobSubCatListView.as_view(), name='job_cat_view'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/pay/', views.pay, name='pay'),
    path('accounts/proposal/', views.proposal, name='proposal'),
    path('accounts/proposal/view/', views.view_proposal, name='view_proposal'),
    path('accounts/login/', views.LoginUserView.as_view(), name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('accounts/settings/', views.ChangeUserInfoView.as_view(), name='settings'),
    path('accounts/settings/change_password', views.ChangePasswordView.as_view(), name='change_password'),
    path('accounts/', views.account_page, name='account'),
    path('accounts/my_chats', views.my_chats, name='my_chats'),
    path('create_job/', views.create_job, name='create_job'),
    path('job/send_proposal/', views.send_proposal, name='send_proposal'),
]
