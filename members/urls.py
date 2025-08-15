from django.urls import path
from . import views

urlpatterns = [
   path('register/' , views.UserRegisterView.as_view() , name='register'),
   path('login/' , views.UserLoginView.as_view() , name='login_page'),
   path('logout/' , views.UserLogoutView.as_view() , name='logout'),
   path('edit-register/' , views.UserEditeRegisterView.as_view() , name='edit_register'),
   path('change-password/' , views.UserChangePasswordView.as_view() , name='change_password'),
   path('profile/<int:pk>/' , views.UserProfilePageView.as_view() , name='profile_page'),
   path('edit-profile/<int:pk>/' , views.UserEditProfilePageView.as_view() , name='edit_profile_page'), 
   path('users-list/' , views.UsersListView.as_view() , name='users_list_page'), 
   path('profile/<int:pk>/follow-request/', views.send_follow_request, name='send_follow_request'),
   path('follow-requests/', views.IncomingFollowRequestsView.as_view(), name='incoming_requests'),
   path('follow-request/<int:request_id>/<str:action>/', 
          views.respond_follow_request, name='respond_follow_request'),
   path('profile/<int:pk>/unfollow/', views.unfollow_user, name='unfollow_user'),
   path('account/archive/',       views.archive_account,   name='archive_account'),
   path('account/unarchive/<int:pk>/', views.unarchive_account, name='unarchive_account'),

]