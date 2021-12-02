class SvoCache:
    """
    Simple cache class around an SvoApi that allows the caller to not repeat requests
    while this cache instance is alive. Cache lifetime is purely controlled by the
    lifetime of this object, there's no timeout in effect.
    """

    def __init__(self, api):
        self.api = api
        self.cache = {}

    def dataset(self, dataset):
        return self._get_cache_entry('dataset', dataset, populate=lambda: self.api.dataset(dataset).get())

    def keywords(self, dataset):
        return self._get_cache_entry('keyword', 'dataset', dataset,
                                     populate=lambda: self.api.keyword.get(limit=0, dataset__name=dataset))

    def data_location(self, dataset, file_url):
        return self._get_cache_entry('data_location', dataset, file_url,
                                     populate=lambda: self.api.data_location.get(
                                         dataset__name=dataset, file_url=file_url))

    def uri(self, uri, limit):
        return self._get_cache_entry('uri', uri, limit, populate=lambda: self.api(uri).get(limit=limit))

    def uri_id(self, uri, id):
        return self._get_cache_entry('uri_id', uri, id, populate=lambda: self.api(uri)(id).get())

    def _get_cache_entry(self, *args, populate=None):
        obj = self.cache
        for i in range(len(args)):
            arg = args[i]

            if arg not in obj:
                if i == len(args) - 1:
                    if populate:
                        obj[arg] = populate()
                    else:
                        raise KeyError('Key %s not found in cache' % arg)
                else:
                    obj[arg] = {}

            obj = obj[arg]

        return obj
