from rest_framework import renderers
import json

# This class Generate the Error the API gives
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetails' in str(data):
            response = json.dumps({'erros':data})
        else:
            response = json.dumps(data)     

        return response