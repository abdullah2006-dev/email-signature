from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_signature, name='create_signature'),
    path('signatures/', views.signature_list, name='signature_list'),
    path('delete/<int:pk>/', views.delete_signature, name='delete_signature'),
    path('select-country/', views.country_select_view, name='select_country'),
    # path('upload-banner/', views.upload_banner, name='upload_banner'),
    # path('banners/', views.banner_list, name='banner_list'),
    # path('banners/delete/<int:pk>/', views.delete_banner, name='confirm_dlete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

