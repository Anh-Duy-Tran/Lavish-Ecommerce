from typing import Iterable, List, Optional, overload

from django.core.exceptions import ValidationError

from ...shipping.models import ShippingMethod
from ..core.utils import from_global_id_or_error


@overload
def get_shipping_model_by_object_id(object_id: str, raise_error=True) -> ShippingMethod:
    ...


@overload
def get_shipping_model_by_object_id(
    object_id: Optional[str], raise_error=False
) -> Optional[ShippingMethod]:
    ...


def get_shipping_model_by_object_id(object_id, raise_error=True):
    if object_id:
        _, object_pk = from_global_id_or_error(object_id)
        shipping_method = ShippingMethod.objects.filter(pk=object_pk).first()
        if not shipping_method and raise_error:
            raise ValidationError(
                {
                    "id": ValidationError(
                        f"Couldn't resolve to a node: {object_id}", code="not_found"
                    )
                }
            )
        return shipping_method
    return None


def get_instances_by_object_ids(object_ids: List[str]) -> Iterable[ShippingMethod]:
    model_ids = []
    for object_id in object_ids:
        _, object_pk = from_global_id_or_error(object_id)
        model_ids.append(object_pk)
    return ShippingMethod.objects.filter(pk__in=model_ids)
