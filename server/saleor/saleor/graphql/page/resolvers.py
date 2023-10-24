from ...page import models
from ..core.utils import from_global_id_or_error
from ..core.validators import validate_one_of_args_is_in_query
from ..utils import get_user_or_app_from_context
from .types import Page


def resolve_page(info, global_page_id=None, slug=None):
    validate_one_of_args_is_in_query("id", global_page_id, "slug", slug)
    requestor = get_user_or_app_from_context(info.context)

    if slug is not None:
        page = models.Page.objects.visible_to_user(requestor).filter(slug=slug).first()
    else:
        _type, page_pk = from_global_id_or_error(global_page_id, Page)
        page = models.Page.objects.visible_to_user(requestor).filter(pk=page_pk).first()
    return page


def resolve_pages(info):
    requestor = get_user_or_app_from_context(info.context)
    return models.Page.objects.visible_to_user(requestor)


def resolve_page_type(id):
    return models.PageType.objects.filter(id=id).first()


def resolve_page_types(_info):
    return models.PageType.objects.all()
