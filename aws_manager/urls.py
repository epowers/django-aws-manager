from aws_manager import views

# DJANGO IMPORTS
try:
    from django.conf.urls import url, patterns
except ImportError:
    try:
        # for Django version less then 1.4
        from django.conf.urls.defaults import url, patterns
    except ImportError:
        # for Django versions greater than 1.8?
        def patterns(ignore, *args):
            return list(args)
        try:
            from django.conf.urls import url
        except ImportError:
            from django.urls import re_path
            def url(*args, **kwargs):
                return re_path(*args, **kwargs)

urlpatterns = patterns('',
    url(r'^get_rdp/(?P<public_dns>[\w|\W]+)/(?P<username>\w+)/$', views.get_rdp),
)

