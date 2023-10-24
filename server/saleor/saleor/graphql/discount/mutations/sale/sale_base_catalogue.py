from collections import defaultdict
from typing import DefaultDict, Set, Union

import graphene
from django.core.exceptions import ValidationError

from .....discount.error_codes import DiscountErrorCode
from .....product.tasks import update_products_discounted_prices_for_promotion_task
from .....product.utils import get_products_ids_without_variants
from ....core import ResolveInfo
from ....core.mutations import BaseMutation
from ....plugins.dataloaders import get_plugin_manager_promise
from ....product.types import Category, Collection, Product, ProductVariant
from ...types import Sale
from ...utils import (
    convert_catalogue_info_into_predicate,
    get_product_ids_for_predicate,
)
from ..voucher.voucher_add_catalogues import CatalogueInput

CatalogueInfo = DefaultDict[str, Set[Union[int, str]]]


class SaleBaseCatalogueMutation(BaseMutation):
    sale = graphene.Field(
        Sale, description="Sale of which catalogue IDs will be modified."
    )

    class Arguments:
        id = graphene.ID(required=True, description="ID of a sale.")
        input = CatalogueInput(
            required=True,
            description="Fields required to modify catalogue IDs of sale.",
        )

    class Meta:
        abstract = True

    @classmethod
    def post_save_actions(
        cls, info: ResolveInfo, promotion, previous_catalogue, new_catalogue
    ):
        if previous_catalogue != new_catalogue:
            manager = get_plugin_manager_promise(info.context).get()
            cls.call_event(
                manager.sale_updated,
                promotion,
                previous_catalogue,
                new_catalogue,
            )

        previous_predicate = convert_catalogue_info_into_predicate(previous_catalogue)
        new_predicate = convert_catalogue_info_into_predicate(new_catalogue)
        previous_product_ids = get_product_ids_for_predicate(previous_predicate)
        new_product_ids = get_product_ids_for_predicate(new_predicate)

        if previous_product_ids != new_product_ids:
            is_add_mutation = len(new_product_ids) > len(previous_product_ids)
            if is_add_mutation:
                product_ids = new_product_ids - previous_product_ids
            else:
                product_ids = previous_product_ids - new_product_ids
            update_products_discounted_prices_for_promotion_task.delay(
                list(product_ids)
            )

    @classmethod
    def get_catalogue_info_from_input(cls, input) -> CatalogueInfo:
        catalogue_info: CatalogueInfo = defaultdict(set)
        if collection_ids := input.get("collections", set()):
            cls.get_nodes_or_error(collection_ids, "collections", Collection)
        if category_ids := input.get("categories", set()):
            cls.get_nodes_or_error(category_ids, "categories", Category)
        if product_ids := input.get("products", set()):
            products = cls.get_nodes_or_error(product_ids, "products", Product)
            cls.clean_product(products)
        if variant_ids := input.get("variants", set()):
            cls.get_nodes_or_error(variant_ids, "variants", ProductVariant)

        catalogue_info["collections"] = set(collection_ids)
        catalogue_info["categories"] = set(category_ids)
        catalogue_info["products"] = set(product_ids)
        catalogue_info["variants"] = set(variant_ids)

        return catalogue_info

    @classmethod
    def clean_product(cls, products):
        products_ids_without_variants = get_products_ids_without_variants(products)
        if products_ids_without_variants:
            error_code = DiscountErrorCode.CANNOT_MANAGE_PRODUCT_WITHOUT_VARIANT.value
            raise ValidationError(
                {
                    "products": ValidationError(
                        "Cannot manage products without variants.",
                        code=error_code,
                        params={"products": products_ids_without_variants},
                    )
                }
            )
