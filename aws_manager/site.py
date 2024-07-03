from .urls import urlpatterns

class AWSManagerSite:
    @property
    def urls(self):
        return urlpatterns, "aws_manager", "aws_manager"

site = AWSManagerSite()
