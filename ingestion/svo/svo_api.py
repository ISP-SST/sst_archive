from slumber import API


class SvoApi(API):
    """
    RESTful API interface for the SVO.
    """

    def __init__(self, api_url, username, api_key):
        self.username = username
        self.api_key = api_key
        super().__init__(api_url, auth=self.api_key_auth)

    def api_key_auth(self, request):
        """
        Sets the API key authentication in the request header.
        """
        request.headers['Authorization'] = 'ApiKey %s:%s' % (self.username, self.api_key)
        return request

    def __call__(self, resource_uri):
        """
        Return a resource from a resource URI.
        """
        return getattr(self, resource_uri)
