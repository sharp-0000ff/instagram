from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'instagram_profile'

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.password_change_form, name='password_change'),
    path('<int:pk>/', views.detail_photography, name='detail_photography'),
    path('create/', views.create_photography_form,
         name='create_photography_form'),
    path('<int:pk>', views.delete_photography, name='delete_photography')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
