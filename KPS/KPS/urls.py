from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'KPS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/login/$', auth_views.login, name='login'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^', include('KPS_app.urls')),
]
