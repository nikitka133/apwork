from django.urls import path

from main import views
from main.views import RegisterUserView, LoginUserView, logout_user, create_job, account_page, ChangeUserInfoView, \
    ChangePasswordView, JobListView, JobSubCatListView, my_chats, send_proposal

urlpatterns = [
    path('', views.index, name='home'),
    path('chat/', views.chat, name='chat'),
    path('job/', JobListView.as_view(), name='job'),
    path('job/<int:pk>', views.job_view, name='job_view'),
    path('job/category/<slug:slug_sub_cat>', JobSubCatListView.as_view(), name='job_cat_view'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path('accounts/settings/', ChangeUserInfoView.as_view(), name='settings'),
    path('accounts/settings/change_password', ChangePasswordView.as_view(), name='change_password'),
    path('accounts/', account_page, name='account'),
    path('accounts/my_chats', my_chats, name='my_chats'),
    path('create_job/', create_job, name='create_job'),
    path('job/send_proposal/', send_proposal, name='send_proposal'),
]
