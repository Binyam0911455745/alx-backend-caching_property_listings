from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetches all properties from the cache or the database.
    """
    properties = cache.get('all_properties')
    if not properties:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties