import random
import string
from django.utils.text import slugify

def random_string_generator(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,new_slug=None):
    """
    this is for a django proj. It assumes that your instance has an model with slug field 
    and a title char field
    """
    if new_slug is not None:
        slug=new_slug
    else:
        slug=slugify(instance.title)
    klass=instance.__class__
    qset_exists=klass.objects.filter(slug=slug).exists()
    if qset_exists:
        new_slug="{slug}-{randstr}".format(
            slug=slug,randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug
