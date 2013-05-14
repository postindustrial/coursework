from django.conf.urls import patterns, include, url

from info.views import home, done, logout, error, form, form2, close_login_popup
from info.facebook import facebook_view
from info.vkontakte import vkontakte_view
from info.odnoklassniki import ok_app, ok_app_info

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coursework.views.home', name='home'),
    # url(r'^coursework/', include('coursework.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'info.views.index'),
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^vk/', vkontakte_view, name='vk_app'),
    url(r'^ok/$', ok_app, name='ok_app'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
    url(r'', include('social_auth.urls')),
)
