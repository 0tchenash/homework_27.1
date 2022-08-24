from django.urls import path
from users.views import *
    
    
urlpatterns = [   
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    # path('create/', CategoryCreateView.as_view()),
    # path('<int:pk>/update/', CategoryUpdateView.as_view()),
    # path('<int:pk>/delete/', CategoryDeleteView.as_view())  
 ]