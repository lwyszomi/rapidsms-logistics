from django import template
from logistics.util import config

register = template.Library()

@register.simple_tag
def breadcrumbs(location):
    mycrumbs = '%(display)s' % \
                {"display": location.name}
    if location.tree_parent is not None:
        # > 
        return '%(parentcrumbs)s &raquo; %(mycrumbs)s' % \
            {"parentcrumbs": breadcrumbs(location.tree_parent),
             "mycrumbs": mycrumbs}
    else:
        return mycrumbs