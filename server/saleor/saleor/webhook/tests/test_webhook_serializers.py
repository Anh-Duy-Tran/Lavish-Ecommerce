from operator import itemgetter
from unittest.mock import ANY, sentinel

import graphene
import pytest

from ...checkout import base_calculations
from ...checkout.fetch import fetch_checkout_info, fetch_checkout_lines
from ...core.prices import quantize_price
from ...discount import DiscountType
from ...discount.utils import (
    create_or_update_discount_objects_from_promotion_for_checkout,
)
from ...plugins.manager import get_plugins_manager
from ...product.models import Product
from ...product.utils.variant_prices import update_discounted_prices_for_promotion
from ..serializers import (
    serialize_checkout_lines,
    serialize_checkout_lines_for_tax_calculation,
    serialize_product_or_variant_attributes,
)


def test_serialize_product_attributes(
    product_with_variant_with_two_attributes, product_with_multiple_values_attributes
):
    variant_data = serialize_product_or_variant_attributes(
        product_with_variant_with_two_attributes.variants.first()
    )
    product_data = serialize_product_or_variant_attributes(
        product_with_multiple_values_attributes
    )
    assert len(variant_data) == 2
    assert variant_data[1] == {
        "entity_type": None,
        "id": ANY,
        "input_type": "dropdown",
        "name": "Size",
        "slug": "size",
        "unit": None,
        "values": [
            {
                "file": None,
                "name": "Small",
                "reference": None,
                "rich_text": None,
                "date_time": None,
                "date": None,
                "boolean": None,
                "slug": "small",
                "value": "",
            }
        ],
    }

    assert len(product_data) == 1
    assert product_data[0]["name"] == "Available Modes"
    assert sorted(product_data[0]["values"], key=itemgetter("name")) == [
        {
            "name": "Eco Mode",
            "slug": "eco",
            "file": None,
            "reference": None,
            "rich_text": None,
            "date_time": None,
            "date": None,
            "boolean": None,
            "value": "",
        },
        {
            "name": "Performance Mode",
            "slug": "power",
            "file": None,
            "reference": None,
            "rich_text": None,
            "date_time": None,
            "date": None,
            "boolean": None,
            "value": "",
        },
    ]


ATTRIBUTES = sentinel.ATTRIBUTES


@pytest.mark.parametrize("taxes_calculated", [True, False])
def test_serialize_checkout_lines(
    checkout_with_items_for_cc, taxes_calculated, site_settings
):
    # given
    checkout = checkout_with_items_for_cc
    channel = checkout.channel
    checkout_lines, _ = fetch_checkout_lines(checkout, prefetch_variant_attributes=True)

    # when
    checkout_lines_data = serialize_checkout_lines(checkout)

    # then
    checkout_with_items_for_cc.refresh_from_db()
    for data, line_info in zip(checkout_lines_data, checkout_lines):
        variant = line_info.line.variant
        product = variant.product
        variant_channel_listing = line_info.channel_listing

        base_price = variant.get_price(variant_channel_listing)
        currency = checkout.currency
        assert data == {
            "sku": variant.sku,
            "quantity": line_info.line.quantity,
            "base_price": str(quantize_price(base_price.amount, currency)),
            "currency": channel.currency_code,
            "full_name": variant.display_product(),
            "product_name": product.name,
            "variant_name": variant.name,
            "attributes": serialize_product_or_variant_attributes(variant),
            "variant_id": variant.get_global_id(),
        }
    assert len(checkout_lines_data) == len(list(checkout_lines))


def test_serialize_checkout_lines_with_promotion(checkout_with_item_on_promotion):
    # given
    checkout = checkout_with_item_on_promotion
    channel = checkout.channel
    checkout_lines, _ = fetch_checkout_lines(checkout, prefetch_variant_attributes=True)

    variant = checkout_lines[0].variant

    create_or_update_discount_objects_from_promotion_for_checkout(checkout_lines)

    # when
    checkout_lines_data = serialize_checkout_lines(checkout)

    # then
    checkout.refresh_from_db()
    assert len(checkout_lines) == 1
    for data, line_info in zip(checkout_lines_data, checkout_lines):
        variant = line_info.line.variant
        product = variant.product
        variant_channel_listing = line_info.channel_listing

        base_price = variant.get_price(variant_channel_listing)
        undiscounted_base_price = variant.get_base_price(variant_channel_listing)
        currency = checkout.currency
        assert base_price < undiscounted_base_price
        assert data == {
            "sku": variant.sku,
            "quantity": line_info.line.quantity,
            "base_price": str(quantize_price(base_price.amount, currency)),
            "currency": channel.currency_code,
            "full_name": variant.display_product(),
            "product_name": product.name,
            "variant_name": variant.name,
            "attributes": serialize_product_or_variant_attributes(variant),
            "variant_id": variant.get_global_id(),
        }
    assert len(checkout_lines_data) == len(list(checkout_lines))


@pytest.mark.parametrize(
    "charge_taxes, prices_entered_with_tax",
    [(False, False), (False, True), (True, False), (True, True)],
)
def test_serialize_checkout_lines_for_tax_calculation(
    checkout_with_prices, charge_taxes, prices_entered_with_tax
):
    # We should be sure that we always sends base prices to tax app.
    # We shouldn't use previously calculated prices because they can be
    # changed by tax app due to e.g.
    # Checkout discount
    # Propagating shipping tax to lines.

    # given
    checkout = checkout_with_prices
    lines, _ = fetch_checkout_lines(checkout)
    manager = get_plugins_manager()
    checkout_info = fetch_checkout_info(checkout, lines, manager)

    tax_configuration = checkout_info.tax_configuration
    tax_configuration.charge_taxes = charge_taxes
    tax_configuration.prices_entered_with_tax = prices_entered_with_tax
    tax_configuration.save(update_fields=["charge_taxes", "prices_entered_with_tax"])
    tax_configuration.country_exceptions.all().delete()

    # when
    checkout_lines_data = serialize_checkout_lines_for_tax_calculation(
        checkout_info, lines
    )

    # then
    for data, line_info in zip(checkout_lines_data, lines):
        line = line_info.line
        variant = line.variant
        product = variant.product

        total_price = base_calculations.calculate_base_line_total_price(
            line_info, checkout_info.channel
        ).amount
        unit_price = base_calculations.calculate_base_line_unit_price(
            line_info, checkout_info.channel
        ).amount

        assert data == {
            "id": graphene.Node.to_global_id("CheckoutLine", line.pk),
            "sku": variant.sku,
            "quantity": line.quantity,
            "charge_taxes": charge_taxes,
            "full_name": variant.display_product(),
            "product_name": product.name,
            "variant_name": variant.name,
            "variant_id": graphene.Node.to_global_id("ProductVariant", variant.pk),
            "product_metadata": product.metadata,
            "product_type_metadata": product.product_type.metadata,
            "unit_amount": unit_price,
            "total_amount": total_price,
        }
    assert len(checkout_lines_data) == len(list(lines))


def test_serialize_checkout_lines_for_tax_calculation_with_promotion(
    checkout_with_prices, promotion_rule, product_list, product
):
    # given
    checkout = checkout_with_prices
    product_list.append(product)
    promotion_rule.catalogue_predicate = {
        "productPredicate": {
            "ids": [
                graphene.Node.to_global_id("Product", product.id)
                for product in product_list
            ]
        },
    }
    promotion_rule.save(update_fields=["catalogue_predicate"])

    update_discounted_prices_for_promotion(Product.objects.all())

    lines, _ = fetch_checkout_lines(checkout)
    manager = get_plugins_manager()
    checkout_info = fetch_checkout_info(checkout, lines, manager)
    create_or_update_discount_objects_from_promotion_for_checkout(lines)

    tax_configuration = checkout_info.tax_configuration
    tax_configuration.country_exceptions.all().delete()

    # when
    checkout_lines_data = serialize_checkout_lines_for_tax_calculation(
        checkout_info, lines
    )

    # then
    for data, line_info in zip(checkout_lines_data, lines):
        line = line_info.line
        variant = line.variant
        product = variant.product

        total_price = base_calculations.calculate_base_line_total_price(
            line_info, checkout_info.channel
        ).amount
        unit_price = base_calculations.calculate_base_line_unit_price(
            line_info, checkout_info.channel
        ).amount

        assert data == {
            "id": graphene.Node.to_global_id("CheckoutLine", line.pk),
            "sku": variant.sku,
            "quantity": line.quantity,
            "charge_taxes": tax_configuration.charge_taxes,
            "full_name": variant.display_product(),
            "product_name": product.name,
            "variant_name": variant.name,
            "variant_id": graphene.Node.to_global_id("ProductVariant", variant.pk),
            "product_metadata": product.metadata,
            "product_type_metadata": product.product_type.metadata,
            "unit_amount": unit_price,
            "total_amount": total_price,
        }

        discount = line_info.discounts[0]
        assert discount.type == DiscountType.PROMOTION
        undiscounted_unit_price = variant.get_base_price(
            line_info.channel_listing,
            line_info.line.price_override,
        ).amount
        assert unit_price < undiscounted_unit_price

    assert len(checkout_lines_data) == len(list(lines))
