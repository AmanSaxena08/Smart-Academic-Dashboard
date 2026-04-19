from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Fix Django 5.x admin logout
admin.site.logout_template = 'admin/logout.html'

urlpatterns = [
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin-logout'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/notices/', include('notices.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)