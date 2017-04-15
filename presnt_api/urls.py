"""presnt_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers, serializers, viewsets
from rest_auth.views import LogoutView, UserDetailsView, PasswordResetView
from presnt_api.views import CustomLoginView as LoginView
from presnt_api.views import CustomRegistrationView as RegistrationView

from presnt_api.router import HybridRouter
from presnt_api import views


router = HybridRouter()
router.register(r'users', views.UserViewSet, 'user')
router.register(r'courses', views.CourseViewSet, 'course')
router.register(r'sections', views.SectionViewSet, 'section')
router.register(r'attendances', views.AttendanceViewSet, 'attendance')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/v2/login', LoginView.as_view(), name='login'),
    url(r'^api/auth/v2/registration', RegistrationView.as_view(), name='registration'),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
]
