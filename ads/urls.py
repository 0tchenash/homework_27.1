
from django.urls import path
from ads.views import *
    
    
urlpatterns = [   
    path('category/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view()),
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdImageView.as_view())    
 ]