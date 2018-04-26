from django.conf.urls import include, url
from django.contrib import admin
from cms import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^update', views.update, name="Update"),
    url(r'^$', views.barra, name='Inicio'),
    url(r'(.+)', views.pag, name='Pagina'),
    url(r'.*', views.error, name='Error'),
]
