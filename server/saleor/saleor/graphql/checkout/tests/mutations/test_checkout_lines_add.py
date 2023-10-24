import datetime
from decimal import Decimal
from unittest import mock

import graphene
import pytest
import pytz
from django.utils import timezone

from .....checkout.error_codes import CheckoutErrorCode
from .....checkout.fetch import fetch_checkout_info, fetch_checkout_lines
from .....checkout.models import Checkout
from .....checkout.utils import (
    calculate_checkout_quantity,
    invalidate_checkout_prices,
    recalculate_checkout_discount,
)
from .....discount import RewardValueType
from .....plugins.manager import get_plugins_manager
from .....product.models import ProductChannelListing
from .....warehouse import WarehouseClickAndCollectOption
from .....warehouse.models import Reservation, Stock
from .....warehouse.tests.utils import get_available_quantity_for_stock
from ....core.utils import to_global_id_or_none
from ....tests.utils import assert_no_permission, get_graphql_content
from ...mutations.utils import update_checkout_shipping_method_if_invalid

MUTATION_CHECKOUT_LINES_ADD = """
mutation checkoutLinesAdd($id: ID, $lines: [CheckoutLineInput!]!) {
  checkoutLinesAdd(id: $id, lines: $lines) {
    checkout {
      token
      discount{
        amount
      }
      quantity
      lines {
        unitPrice {
          gross {
            amount
          }
        }
        totalPrice {
          gross {
            amount
          }
        }
        undiscountedTotalPrice {
          amount
        }
        undiscountedUnitPrice {
          amount
        }
        quantity
        variant {
          id
        }
      }
    }
    errors {
      field
      code
      message
      variants
    }
  }
}
"""


@mock.patch(
    "saleor.graphql.checkout.mutations.checkout_lines_add."
    "update_checkout_shipping_method_if_invalid",
    wraps=update_checkout_shipping_method_if_invalid,
)
@mock.patch(
    "saleor.graphql.checkout.mutations.checkout_lines_add."
    "invalidate_checkout_prices",
    wraps=invalidate_checkout_prices,
)
def test_checkout_lines_add(
    mocked_invalidate_checkout_prices,
    mocked_update_shipping_method,
    user_api_client,
    checkout_with_item,
    stock,
):
    # given
    variant = stock.product_variant
    checkout = checkout_with_item

    line = checkout.lines.first()
    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    previous_last_change = checkout.last_change

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    lines, _ = fetch_checkout_lines(checkout)
    line = checkout.lines.last()
    assert line.variant == variant
    assert line.quantity == 1
    assert calculate_checkout_quantity(lines) == 4
    assert not Reservation.objects.exists()

    manager = get_plugins_manager()
    lines, _ = fetch_checkout_lines(checkout)
    checkout_info = fetch_checkout_info(checkout, lines, manager)
    mocked_update_shipping_method.assert_called_once_with(checkout_info, lines)
    assert checkout.last_change != previous_last_change
    assert mocked_invalidate_checkout_prices.call_count == 1


@mock.patch(
    "saleor.graphql.checkout.mutations.checkout_lines_add."
    "update_checkout_shipping_method_if_invalid",
    wraps=update_checkout_shipping_method_if_invalid,
)
@mock.patch(
    "saleor.graphql.checkout.mutations.checkout_lines_add."
    "invalidate_checkout_prices",
    wraps=invalidate_checkout_prices,
)
def test_add_to_existing_line_with_sale_when_checkout_has_voucher(
    mocked_invalidate_checkout_prices,
    mocked_update_shipping_method,
    user_api_client,
    checkout_with_item,
    stock,
    voucher_percentage,
    channel_USD,
    promotion_without_rules,
):
    # given

    # prepare voucher with 50% discount
    voucher_percentage_value = 50
    voucher_percentage.channel_listings.update(discount_value=voucher_percentage_value)

    checkout = checkout_with_item
    checkout.voucher_code = voucher_percentage.code
    checkout.save()

    variant_unit_price = Decimal(100)
    line = checkout.lines.first()
    variant = line.variant

    # prepare promotion with 50% discount

    reward_value = Decimal("50.00")
    rule = promotion_without_rules.rules.create(
        catalogue_predicate={
            "productPredicate": {
                "ids": [graphene.Node.to_global_id("Product", variant.product.id)]
            }
        },
        reward_value_type=RewardValueType.PERCENTAGE,
        reward_value=reward_value,
    )
    rule.channels.add(channel_USD)

    variant_channel_listing = variant.channel_listings.get(channel=channel_USD)

    variant_channel_listing.price_amount = variant_unit_price
    discount_amount = variant_unit_price * reward_value / 100
    variant_channel_listing.discounted_price_amount = (
        variant_channel_listing.price_amount - discount_amount
    )
    variant_channel_listing.save(
        update_fields=["discounted_price_amount", "price_amount"]
    )

    variant_channel_listing.variantlistingpromotionrule.create(
        promotion_rule=rule,
        discount_amount=discount_amount,
        currency=channel_USD.currency_code,
    )

    # create checkout discount objects for checkout lines
    manager = get_plugins_manager()
    lines_infos, _ = fetch_checkout_lines(checkout)
    checkout_info = fetch_checkout_info(checkout, lines_infos, manager)
    recalculate_checkout_discount(manager, checkout_info, lines_infos)

    variant_id = graphene.Node.to_global_id("ProductVariant", line.variant_id)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    # then
    # unit_price: 100, sale 50% then voucher 50% = 25
    expected_unit_price_after_all_discount = Decimal(25)

    expected_discount_per_single_item = Decimal(25)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    print(data)
    assert not data["errors"]
    checkout.refresh_from_db()
    lines, _ = fetch_checkout_lines(checkout)
    line = checkout.lines.last()
    assert (
        line.total_price_gross_amount
        == expected_unit_price_after_all_discount * line.quantity
    )
    assert (
        line.total_price_net_amount
        == expected_unit_price_after_all_discount * line.quantity
    )
    unit_price = data["checkout"]["lines"][0]["unitPrice"]["gross"]["amount"]
    assert Decimal(unit_price) == expected_unit_price_after_all_discount
    total_price = data["checkout"]["lines"][0]["totalPrice"]["gross"]["amount"]
    assert (
        Decimal(total_price) == expected_unit_price_after_all_discount * line.quantity
    )
    checkout_discount_amount = data["checkout"]["discount"]["amount"]
    # unit price is 50 USD, (after applying sale), then 50% voucher gives us a
    # unit_price equal to 25 USD. The discount amount is 25 USD * quantity
    assert (
        Decimal(checkout_discount_amount)
        == expected_discount_per_single_item * line.quantity
    )


def test_checkout_lines_add_with_existing_variant_and_metadata(
    user_api_client,
    checkout_with_item,
    stock,
):
    # given
    checkout = checkout_with_item

    old_meta = {"old_key": "old_value"}
    metadata_key = "md key"
    metadata_value = "md value"

    line = checkout.lines.first()
    line.store_value_in_metadata(old_meta)
    line.save(update_fields=["metadata"])

    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", line.variant_id)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [
            {
                "variantId": variant_id,
                "quantity": 1,
                "metadata": [{"key": metadata_key, "value": metadata_value}],
            }
        ],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    checkout.refresh_from_db()
    line.refresh_from_db()

    # then
    assert not data["errors"]
    assert line.quantity == 4
    assert line.metadata == {**old_meta, **{metadata_key: metadata_value}}


def test_checkout_lines_add_with_new_variant_and_metadata(
    user_api_client,
    checkout_with_item,
    stock,
):
    # given
    variant = stock.product_variant

    checkout = checkout_with_item

    metadata_key = "md key"
    metadata_value = "md value"

    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [
            {
                "variantId": variant_id,
                "quantity": 1,
                "metadata": [{"key": metadata_key, "value": metadata_value}],
            }
        ],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    checkout.refresh_from_db()
    line = checkout.lines.last()

    # then
    assert not data["errors"]
    assert checkout.lines.count() == 2
    assert line.variant == variant
    assert line.quantity == 1
    assert line.metadata == {metadata_key: metadata_value}


@mock.patch(
    "saleor.graphql.checkout.mutations.checkout_lines_add."
    "update_checkout_shipping_method_if_invalid",
    wraps=update_checkout_shipping_method_if_invalid,
)
def test_checkout_lines_add_only_stock_in_cc_warehouse(
    mocked_update_shipping_method, user_api_client, checkout_with_item, warehouse_for_cc
):
    """Ensure the line can be added to the checkout when the only available quantity
    is in a stock from the collection point warehouse without shipping zone assigned."""
    # given
    checkout = checkout_with_item

    line = checkout.lines.first()
    variant = line.variant
    variant.stocks.all().delete()

    Stock.objects.create(
        warehouse=warehouse_for_cc, product_variant=variant, quantity=10
    )

    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    previous_last_change = checkout.last_change

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    lines, _ = fetch_checkout_lines(checkout)
    assert len(lines) == 1
    line = lines[0].line
    assert line.variant == variant
    assert line.quantity == 4
    assert calculate_checkout_quantity(lines) == 4
    assert not Reservation.objects.exists()

    manager = get_plugins_manager()
    checkout_info = fetch_checkout_info(checkout, lines, manager)
    mocked_update_shipping_method.assert_called_once_with(checkout_info, lines)
    assert checkout.last_change != previous_last_change


def test_checkout_lines_add_only_stock_in_cc_warehouse_delivery_method_set(
    user_api_client, checkout_with_item, warehouse_for_cc, shipping_method
):
    """Ensure the insufficient error is raised when the only available quantity is in
    a stock from the collection point warehouse without shipping zone assigned
    and the checkout has shipping method set."""
    # given
    checkout = checkout_with_item

    line = checkout.lines.first()
    variant = line.variant
    variant.stocks.all().delete()

    # set stock for a collection point warehouse
    Stock.objects.create(
        warehouse=warehouse_for_cc, product_variant=variant, quantity=10
    )

    checkout.shipping_method = shipping_method
    checkout.save(update_fields=["shipping_method"])

    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert data["errors"]
    assert data["errors"][0]["code"] == CheckoutErrorCode.INSUFFICIENT_STOCK.name
    assert data["errors"][0]["field"] == "quantity"


def test_checkout_lines_add_with_reservations(
    site_settings_with_reservations, user_api_client, checkout_with_item, stock
):
    variant = stock.product_variant
    checkout = checkout_with_item
    line = checkout.lines.first()
    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    lines, _ = fetch_checkout_lines(checkout)
    line = checkout.lines.last()
    assert line.variant == variant
    assert line.quantity == 1
    assert calculate_checkout_quantity(lines) == 4

    reservation = line.reservations.get()
    assert reservation
    assert reservation.checkout_line == line
    assert reservation.quantity_reserved == line.quantity


def test_checkout_lines_add_updates_reservation(
    site_settings_with_reservations,
    user_api_client,
    checkout_line_with_one_reservation,
    stock,
):
    variant = checkout_line_with_one_reservation.variant
    checkout = checkout_line_with_one_reservation.checkout
    line = checkout_line_with_one_reservation
    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 2
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    lines, _ = fetch_checkout_lines(checkout)
    line = checkout.lines.last()
    assert line.variant == variant
    assert line.quantity == 3
    assert calculate_checkout_quantity(lines) == 3

    reservation = line.reservations.get()
    assert reservation
    assert reservation.checkout_line == line
    assert reservation.quantity_reserved == line.quantity


def test_checkout_lines_add_new_variant_updates_other_lines_reservations_expirations(
    site_settings_with_reservations,
    user_api_client,
    checkout_line_with_one_reservation,
    product,
    warehouse,
):
    variant = checkout_line_with_one_reservation.variant
    checkout = checkout_line_with_one_reservation.checkout
    line = checkout_line_with_one_reservation
    reservation = line.reservations.get()

    lines, _ = fetch_checkout_lines(checkout)
    assert calculate_checkout_quantity(lines) == 2

    variant_other = product.variants.create(sku="SKU_B")
    variant_other.channel_listings.create(
        channel=checkout.channel,
        price_amount=Decimal(10),
        cost_price_amount=Decimal(1),
        currency=checkout.channel.currency_code,
    )
    Stock.objects.create(
        product_variant=variant_other, warehouse=warehouse, quantity=15
    )
    variant_other_id = graphene.Node.to_global_id("ProductVariant", variant_other.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_other_id, "quantity": 3}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    reservation.refresh_from_db()

    assert not data["errors"]
    checkout.refresh_from_db()
    lines, _ = fetch_checkout_lines(checkout)
    line.refresh_from_db()
    assert line.variant == variant
    assert line.quantity == 2
    new_line = checkout.lines.get(variant=variant_other)
    assert new_line.variant == variant_other
    assert new_line.quantity == 3
    assert calculate_checkout_quantity(lines) == 5

    other_reservation = Reservation.objects.get(checkout_line__variant=variant_other)
    assert other_reservation.checkout_line == new_line
    assert other_reservation.quantity_reserved == new_line.quantity
    assert reservation.reserved_until == other_reservation.reserved_until


def test_checkout_lines_add_existing_variant(user_api_client, checkout_with_item):
    checkout = checkout_with_item
    line = checkout.lines.first()
    variant_id = graphene.Node.to_global_id("ProductVariant", line.variant.pk)
    previous_last_change = checkout.last_change

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 7}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    line = checkout.lines.last()
    assert line.quantity == 10
    assert checkout.last_change != previous_last_change


def test_checkout_lines_add_with_force_new_line(
    app_api_client, checkout, stock, permission_handle_checkouts
):
    # given
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [
            {"variantId": variant_id, "quantity": 1},
            {"variantId": variant_id, "quantity": 1, "forceNewLine": True},
        ],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = app_api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
        permissions=[permission_handle_checkouts],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    checkout.refresh_from_db()
    lines = checkout.lines.all()

    # then
    assert not data["errors"]
    assert len(lines) == 2
    for line in lines:
        assert line.variant == variant
        assert line.quantity == 1


def test_checkout_lines_add_create_new_line_when_variant_already_in_multiple_lines(
    app_api_client,
    checkout_with_same_items_in_multiple_lines,
    permission_handle_checkouts,
):
    # given
    checkout = checkout_with_same_items_in_multiple_lines
    assert checkout.lines.count() == 2

    variant_id = checkout.lines.first().variant_id
    variant_global_id = graphene.Node.to_global_id("ProductVariant", variant_id)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [
            {"variantId": variant_global_id, "quantity": 1},
        ],
        "channelSlug": checkout.channel.slug,
    }

    # when
    response = app_api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
        permissions=[permission_handle_checkouts],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    checkout.refresh_from_db()
    lines = checkout.lines.all()

    # then
    assert not data["errors"]
    assert len(lines) == 3

    for line in lines:
        assert line.variant_id == variant_id
        assert line.quantity == 1


def test_checkout_lines_add_custom_price(
    app_api_client, checkout, stock, permission_handle_checkouts
):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    price = Decimal("13.11")

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1, "price": price}],
        "channelSlug": checkout.channel.slug,
    }
    response = app_api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
        permissions=[permission_handle_checkouts],
    )
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    line = checkout.lines.last()
    assert line.variant == variant
    assert line.quantity == 1
    assert line.price_override == price


def test_checkout_lines_add_existing_variant_with_custom_price(
    app_api_client, checkout_with_item, permission_handle_checkouts
):
    checkout = checkout_with_item
    line = checkout.lines.first()
    variant_id = graphene.Node.to_global_id("ProductVariant", line.variant.pk)
    price = Decimal("13.11")

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 7, "price": price}],
        "channelSlug": checkout.channel.slug,
    }
    response = app_api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
        permissions=[permission_handle_checkouts],
    )
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    line = checkout.lines.last()
    assert line.quantity == 10
    assert line.price_override == price


def test_checkout_lines_add_existing_variant_override_previous_custom_price(
    app_api_client, checkout_with_item, permission_handle_checkouts
):
    checkout = checkout_with_item
    line = checkout.lines.first()
    line.price_override = 8.22
    line.save(update_fields=["price_override"])

    variant_id = graphene.Node.to_global_id("ProductVariant", line.variant.pk)
    price = Decimal("13.11")

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 7, "price": price}],
        "channelSlug": checkout.channel.slug,
    }
    response = app_api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
        permissions=[permission_handle_checkouts],
    )
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    line = checkout.lines.last()
    assert line.quantity == 10
    assert line.price_override == price


def test_checkout_lines_add_custom_price_app_no_perm(app_api_client, checkout, stock):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    price = Decimal("13.11")

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1, "price": price}],
        "channelSlug": checkout.channel.slug,
    }
    response = app_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    assert_no_permission(response)


def test_checkout_lines_add_custom_price_permission_denied_for_staff_user(
    staff_api_client, checkout, stock, permission_handle_checkouts
):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    price = Decimal("13.11")

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1, "price": price}],
        "channelSlug": checkout.channel.slug,
    }
    response = staff_api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
        permissions=[permission_handle_checkouts],
    )
    assert_no_permission(response)


def test_checkout_lines_add_existing_variant_over_allowed_stock(
    user_api_client, checkout_with_item
):
    checkout = checkout_with_item
    line = checkout.lines.first()
    variant_id = graphene.Node.to_global_id("ProductVariant", line.variant.pk)
    current_stock = line.variant.stocks.first()

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": current_stock.quantity - 1}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    errors = content["data"]["checkoutLinesAdd"]["errors"]
    assert errors[0]["code"] == CheckoutErrorCode.INSUFFICIENT_STOCK.name


def test_checkout_lines_add_with_unavailable_variant(
    user_api_client, checkout_with_item, stock
):
    variant = stock.product_variant
    variant.channel_listings.filter(channel=checkout_with_item.channel).update(
        price_amount=None
    )
    checkout = checkout_with_item
    line = checkout.lines.first()
    assert line.quantity == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    errors = content["data"]["checkoutLinesAdd"]["errors"]
    assert errors[0]["code"] == CheckoutErrorCode.UNAVAILABLE_VARIANT_IN_CHANNEL.name
    assert errors[0]["field"] == "lines"
    assert errors[0]["variants"] == [variant_id]


def test_checkout_lines_add_with_insufficient_stock(
    user_api_client, checkout_with_item, stock
):
    variant = stock.product_variant
    checkout = checkout_with_item
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 49}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    errors = content["data"]["checkoutLinesAdd"]["errors"]
    assert errors[0]["code"] == CheckoutErrorCode.INSUFFICIENT_STOCK.name
    assert errors[0]["field"] == "quantity"


def test_checkout_lines_add_with_reserved_insufficient_stock(
    site_settings_with_reservations,
    user_api_client,
    checkout_with_item,
    stock,
    channel_USD,
):
    variant = stock.product_variant
    checkout = checkout_with_item
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    quantity_available = get_available_quantity_for_stock(stock)

    other_checkout = Checkout.objects.create(channel=channel_USD, currency="USD")
    other_checkout_line = other_checkout.lines.create(
        variant=variant,
        quantity=quantity_available - 1,
    )
    Reservation.objects.create(
        checkout_line=other_checkout_line,
        stock=stock,
        quantity_reserved=quantity_available - 1,
        reserved_until=timezone.now() + datetime.timedelta(minutes=5),
    )

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 2}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    errors = content["data"]["checkoutLinesAdd"]["errors"]
    assert errors[0]["code"] == CheckoutErrorCode.INSUFFICIENT_STOCK.name
    assert errors[0]["field"] == "quantity"


@pytest.mark.parametrize(
    "cc_option",
    [
        WarehouseClickAndCollectOption.ALL_WAREHOUSES,
        WarehouseClickAndCollectOption.LOCAL_STOCK,
    ],
)
def test_checkout_lines_for_click_and_collect_insufficient_stock(
    user_api_client, checkout_with_item_for_cc, warehouse_for_cc, cc_option
):
    checkout = checkout_with_item_for_cc
    checkout.collection_point = warehouse_for_cc

    warehouse_for_cc.click_and_collect_option = cc_option
    warehouse_for_cc.save(update_fields=["click_and_collect_option"])
    checkout.refresh_from_db()

    variant = checkout.lines.last().variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 42}],
        "channelSlug": checkout.channel.slug,
    }

    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    errors = content["data"]["checkoutLinesAdd"]["errors"]

    assert errors[0]["code"] == CheckoutErrorCode.INSUFFICIENT_STOCK.name
    assert errors[0]["field"] == "quantity"


def test_checkout_lines_add_with_zero_quantity(
    user_api_client, checkout_with_item, stock
):
    variant = stock.product_variant
    checkout = checkout_with_item
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 0}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    errors = content["data"]["checkoutLinesAdd"]["errors"]
    assert errors[0]["code"] == CheckoutErrorCode.ZERO_QUANTITY.name
    assert errors[0]["field"] == "quantity"


def test_checkout_lines_add_no_channel_shipping_zones(
    user_api_client, checkout_with_item, stock
):
    variant = stock.product_variant
    checkout = checkout_with_item
    checkout.channel.shipping_zones.clear()
    line = checkout.lines.first()
    assert line.quantity == 3
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)

    data = content["data"]["checkoutLinesAdd"]
    errors = data["errors"]
    assert len(errors) == 1
    assert errors[0]["code"] == CheckoutErrorCode.INSUFFICIENT_STOCK.name
    assert errors[0]["field"] == "quantity"


def test_checkout_lines_add_with_unpublished_product(
    user_api_client, checkout_with_item, stock, channel_USD
):
    variant = stock.product_variant
    product = variant.product
    ProductChannelListing.objects.filter(product=product, channel=channel_USD).update(
        is_published=False
    )

    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout_with_item),
        "lines": [{"variantId": variant_id, "quantity": 1}],
        "channelSlug": checkout_with_item.channel.slug,
    }

    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    content = get_graphql_content(response)
    error = content["data"]["checkoutLinesAdd"]["errors"][0]
    assert error["code"] == CheckoutErrorCode.PRODUCT_NOT_PUBLISHED.name


def test_checkout_lines_add_with_unavailable_for_purchase_product(
    user_api_client, checkout_with_item, stock
):
    # given
    variant = stock.product_variant
    product = stock.product_variant.product
    product.channel_listings.update(available_for_purchase_at=None)

    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout_with_item),
        "lines": [{"variantId": variant_id, "quantity": 1}],
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    # then
    content = get_graphql_content(response)
    error = content["data"]["checkoutLinesAdd"]["errors"][0]
    assert error["field"] == "lines"
    assert error["code"] == CheckoutErrorCode.PRODUCT_UNAVAILABLE_FOR_PURCHASE.name
    assert error["variants"] == [variant_id]


def test_checkout_lines_add_with_available_for_purchase_from_tomorrow_product(
    user_api_client, checkout_with_item, stock
):
    # given
    variant = stock.product_variant
    product = stock.product_variant.product
    product.channel_listings.update(
        available_for_purchase_at=datetime.datetime.now(pytz.UTC)
        + datetime.timedelta(days=1)
    )

    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout_with_item),
        "lines": [{"variantId": variant_id, "quantity": 1}],
    }

    # when
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)

    # then
    content = get_graphql_content(response)
    error = content["data"]["checkoutLinesAdd"]["errors"][0]
    assert error["field"] == "lines"
    assert error["code"] == CheckoutErrorCode.PRODUCT_UNAVAILABLE_FOR_PURCHASE.name
    assert error["variants"] == [variant_id]


def test_checkout_lines_add_too_many(user_api_client, checkout_with_item, stock):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout_with_item),
        "lines": [{"variantId": variant_id, "quantity": 51}],
        "channelSlug": checkout_with_item.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)["data"]["checkoutLinesAdd"]

    assert content["errors"]
    assert content["errors"] == [
        {
            "field": "quantity",
            "message": "Cannot add more than 50 times this item: SKU_A.",
            "code": "QUANTITY_GREATER_THAN_LIMIT",
            "variants": None,
        }
    ]


def test_checkout_lines_add_too_many_when_variant_in_multiple_lines(
    user_api_client, checkout_with_item, stock
):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout_with_item),
        "lines": [
            {"variantId": variant_id, "quantity": 30},
            {"variantId": variant_id, "quantity": 21, "forceNewLine": True},
        ],
        "channelSlug": checkout_with_item.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)["data"]["checkoutLinesAdd"]

    assert content["errors"]
    assert content["errors"] == [
        {
            "field": "quantity",
            "message": "Cannot add more than 50 times this item: SKU_A.",
            "code": "QUANTITY_GREATER_THAN_LIMIT",
            "variants": None,
        }
    ]


@pytest.mark.parametrize("is_preorder", [True, False])
def test_checkout_lines_add_too_many_after_two_trials(
    user_api_client, checkout_with_item, stock, is_preorder
):
    variant = stock.product_variant
    variant.is_preorder = is_preorder
    variant.preorder_end_date = timezone.now() + datetime.timedelta(days=1)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    stock.quantity = 200
    stock.save(update_fields=["quantity"])
    variant.save(update_fields=["is_preorder", "preorder_end_date"])

    variables = {
        "id": to_global_id_or_none(checkout_with_item),
        "lines": [{"variantId": variant_id, "quantity": 26}],
        "channelSlug": checkout_with_item.channel.slug,
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)["data"]["checkoutLinesAdd"]

    assert not content["errors"]

    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)["data"]["checkoutLinesAdd"]

    assert content["errors"] == [
        {
            "field": "quantity",
            "message": "Cannot add more than 50 times this item: SKU_A.",
            "code": "QUANTITY_GREATER_THAN_LIMIT",
            "variants": None,
        }
    ]


def test_checkout_lines_add_empty_checkout(user_api_client, checkout, stock):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    line = checkout.lines.first()
    assert line.variant == variant
    assert line.quantity == 1


def test_checkout_lines_add_variant_without_inventory_tracking(
    user_api_client, checkout, variant_without_inventory_tracking
):
    variant = variant_without_inventory_tracking
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 1}],
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert not data["errors"]
    checkout.refresh_from_db()
    line = checkout.lines.first()
    assert line.variant == variant
    assert line.quantity == 1


def test_checkout_lines_add_check_lines_quantity(user_api_client, checkout, stock):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [{"variantId": variant_id, "quantity": 16}],
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    assert data["errors"][0]["message"] == (
        "Could not add items SKU_A. Only 15 remaining in stock."
    )
    assert data["errors"][0]["field"] == "quantity"


def test_checkout_lines_invalid_variant_id(user_api_client, checkout, stock):
    variant = stock.product_variant
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.pk)
    invalid_variant_id = "InvalidId"

    variables = {
        "id": to_global_id_or_none(checkout),
        "lines": [
            {"variantId": variant_id, "quantity": 1},
            {"variantId": invalid_variant_id, "quantity": 3},
        ],
    }
    response = user_api_client.post_graphql(MUTATION_CHECKOUT_LINES_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["checkoutLinesAdd"]
    error_msg = (
        "Could not resolve to a node with the global id list of "
        f"'['{invalid_variant_id}']'."
    )
    assert data["errors"][0]["message"] == error_msg
    assert data["errors"][0]["field"] == "variantId"


def test_with_active_problems_flow(
    api_client, checkout_with_problems, product_with_single_variant
):
    # given
    channel = checkout_with_problems.channel
    channel.use_legacy_error_flow_for_checkout = False
    channel.save(update_fields=["use_legacy_error_flow_for_checkout"])

    variant = product_with_single_variant.variants.first()

    variables = {
        "id": to_global_id_or_none(checkout_with_problems),
        "lines": [{"variantId": to_global_id_or_none(variant), "quantity": 1}],
    }

    # when
    response = api_client.post_graphql(
        MUTATION_CHECKOUT_LINES_ADD,
        variables,
    )
    content = get_graphql_content(response)

    # then
    assert not content["data"]["checkoutLinesAdd"]["errors"]
