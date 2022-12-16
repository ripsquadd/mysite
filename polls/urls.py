from django.urls import path

from . import views
from .views import RegisterView, profile, LoginView, LogoutView, ChangeUserView, PasswordChangeView, DeleteUserView

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/delete/', DeleteUserView.as_view(), name='delete'),
    path('profile/change/', ChangeUserView.as_view(), name='change'),
    path('profile/', profile, name='profile'),
    path('profile/password/change/', PasswordChangeView.as_view(), name='password_change'),
]

