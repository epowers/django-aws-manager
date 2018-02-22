from aws_manager import views

# DJANGO IMPORTS
try:
    from django.conf.urls import url, patterns
except ImportError:
    try:
        # for Django version less then 1.4
        from django.conf.urls.defaults import url, patterns
    except:
        # for Django versions greater than 1.8?
        from django.conf.urls import url
        def patterns(ignore, *args):
            return list(args)

urlpatterns = patterns('',
    url(r'^get_rdp/(?P<public_dns>[\w|\W]+)/(?P<username>\w+)/$', views.get_rdp),
)

