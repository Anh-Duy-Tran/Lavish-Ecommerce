from typing import List, Tuple

import graphene

from .....attribute import models as attribute_models
from .....permission.enums import ProductPermissions
from .....product import models
from .....product.tasks import update_products_discounted_prices_for_promotion_task
from ....attribute.utils import AttributeAssignmentMixin, AttrValuesInput
from ....core import ResolveInfo
from ....core.descriptions import ADDED_IN_310
from ....core.mutations import ModelWithExtRefMutation
from ....core.types.common import ProductError
from ....plugins.dataloaders import get_plugin_manager_promise
from ...types import Product
from .product_create import ProductCreate, ProductInput

T_INPUT_MAP = List[Tuple[attribute_models.Attribute, AttrValuesInput]]


class ProductUpdate(ProductCreate, ModelWithExtRefMutation):
    class Arguments:
        id = graphene.ID(required=False, description="ID of a product to update.")
        external_reference = graphene.String(
            required=False,
            description=f"External ID of a product to update. {ADDED_IN_310}",
        )
        input = ProductInput(
            required=True, description="Fields required to update a product."
        )

    class Meta:
        description = "Updates an existing product."
        model = models.Product
        object_type = Product
        permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"
        support_meta_field = True
        support_private_meta_field = True

    @classmethod
    def clean_attributes(
        cls, attributes: dict, product_type: models.ProductType
    ) -> T_INPUT_MAP:
        attributes_qs = product_type.product_attributes.all()
        attributes = AttributeAssignmentMixin.clean_input(
            attributes, attributes_qs, creation=False
        )
        return attributes

    @classmethod
    def post_save_action(cls, info: ResolveInfo, instance, cleaned_input):
        product = models.Product.objects.prefetched_for_webhook().get(pk=instance.pk)
        if "category" in cleaned_input or "collections" in cleaned_input:
            update_products_discounted_prices_for_promotion_task.delay([instance.id])
        manager = get_plugin_manager_promise(info.context).get()
        cls.call_event(manager.product_updated, product)

    @classmethod
    def get_instance(cls, info, **data):
        """Prefetch related fields that are needed to process the mutation."""
        # If we are updating an instance and want to update its attributes,
        # prefetch them.
        object_id = cls.get_object_id(**data)
        if object_id and data.get("attributes"):
            # Prefetches needed by AttributeAssignmentMixin and
            # associate_attribute_values_to_instance
            qs = cls.Meta.model.objects.prefetch_related(
                "product_type__product_attributes__values",
                "product_type__attributeproduct",
            )
            return cls.get_node_or_error(info, object_id, only_type="Product", qs=qs)

        return super().get_instance(info, **data)
