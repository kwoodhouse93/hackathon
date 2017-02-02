"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache
from hackathon.views import RegistrationView
from ckeditor_uploader import views as ckeu_views

urlpatterns = [
    url(r'^', include('projects.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^hackathons/', include('hackathons.urls', namespace="hackathons")),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name':'auth/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, name='auth_logout'),
    url(r'^signup/complete/$',
        TemplateView.as_view(template_name='auth/signup_complete.html'),
        name='auth_signup_complete'),
    url(r'^signup/$',
        RegistrationView.as_view(),
        name='auth_signup'),
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^upload/', ckeu_views.upload, name='ckeditor_upload'),
    url(r'^browse/', never_cache(ckeu_views.browse), name='ckeditor_browse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)