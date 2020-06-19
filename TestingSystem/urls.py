from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from accounts.views import login_view, logout_view, signup_view, generate_view

urlpatterns = [
    # переопределили своим шаблоном
    path('admin/login/', views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('admin/logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace='app'))
]
