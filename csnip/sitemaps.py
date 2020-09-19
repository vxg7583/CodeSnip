from django.contrib.sitemaps import Sitemap
from .models import Snippet

class SnippetSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Snippet.publishedd.all()

    def lastmod(self, obj):
        return obj.updated
