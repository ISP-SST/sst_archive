from django.core.cache import caches


def get_memory_cache():
    return caches['memory']
