from rest_framework import renderers

class TagRenderer(renderers.BaseRenderer):
    media_type = 'text/csv'
    format='csv'

    def render(self,data,accepted_media_type=None, renderer_context=None):
        return data