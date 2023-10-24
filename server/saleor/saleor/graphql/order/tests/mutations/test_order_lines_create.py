from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

import graphene
import pytest
import pytz
from django.db.models import Sum

from .....discount import DiscountType, RewardValueType
from .....order import OrderStatus
from .....order import events as order_events
from .....order.error_codes import OrderErrorCode
from .....order.models import OrderEvent, OrderLine
from .....product.models import ProductVariant
from .....warehouse.models import Allocation, Stock
from ....tests.utils import assert_no_permission, get_graphql_content
from ..utils import assert_proper_webhook_called_once

ORDER_LINES_CREATE_MUTATION = """
    mutation OrderLinesCreate(
            $orderId: ID!,
            $variantId: ID!,
            $quantity: Int!,
            $forceNewLine: Boolean,
            $price: PositiveDecimal,
        ) {
        orderLinesCreate(id: $orderId,
                input: [
                    {
                        variantId: $variantId,
                        quantity: $quantity,
                        forceNewLine: $forceNewLine,
                        price: $price
                    }
                ]) {

            errors {
                field
                code
                message
                variants
            }
            orderLines {
                id
                quantity
                productSku
                productVariantId
                saleId
                unitPrice {
                    gross {
                        amount
                        currency
                    }
                    net {
                        amount
                        currency
                    }
                }
            }
            order {
                total {
                    gross {
                        amount
                    }
                }
            }
        }
    }
"""


@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
def test_order_lines_create_with_out_of_stock_webhook(
    product_variant_out_of_stock_webhook_mock,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
):
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status"])
    line = order.lines.first()
    variant = line.variant
    quantity = 2
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    permission_group_manage_orders.user_set.add(staff_api_client.user)
    staff_api_client.post_graphql(query, variables)

    quantity_allocated = Allocation.objects.aggregate(Sum("quantity_allocated"))[
        "quantity_allocated__sum"
    ]
    stock_quantity = Allocation.objects.aggregate(Sum("stock__quantity"))[
        "stock__quantity__sum"
    ]
    assert quantity_allocated == stock_quantity
    product_variant_out_of_stock_webhook_mock.assert_called_once_with(
        Stock.objects.first()
    )


@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
def test_order_lines_create_for_variant_with_many_stocks_with_out_of_stock_webhook(
    product_variant_out_of_stock_webhook_mock,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant_with_many_stocks,
):
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status"])
    variant = variant_with_many_stocks
    quantity = 4
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    permission_group_manage_orders.user_set.add(staff_api_client.user)
    staff_api_client.post_graphql(query, variables)
    product_variant_out_of_stock_webhook_mock.assert_called_once_with(
        Stock.objects.all()[3]
    )


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
def test_order_lines_create(
    product_variant_out_of_stock_webhook_mock,
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant_with_many_stocks,
):
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    variant = variant_with_many_stocks
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    # mutation should fail without proper permissions
    response = staff_api_client.post_graphql(query, variables)
    assert_no_permission(response)
    order_updated_webhook_mock.assert_not_called()
    draft_order_updated_webhook_mock.assert_not_called()
    assert not OrderEvent.objects.exists()

    # assign permissions
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(query, variables)
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )
    assert OrderEvent.objects.count() == 1
    event = OrderEvent.objects.last()
    assert event.type == order_events.OrderEvents.ADDED_PRODUCTS
    assert len(event.parameters["lines"]) == 1
    line = OrderLine.objects.last()
    assert event.parameters["lines"] == [
        {"item": str(line), "line_pk": str(line.pk), "quantity": quantity}
    ]

    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity

    # mutation should fail when quantity is lower than 1
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": 0}
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["errors"]
    assert data["errors"][0]["field"] == "quantity"
    assert data["errors"][0]["variants"] == [variant_id]
    product_variant_out_of_stock_webhook_mock.assert_not_called()


def test_order_lines_create_by_user_no_channel_access(
    order_with_lines,
    permission_group_all_perms_channel_USD_only,
    staff_api_client,
    variant_with_many_stocks,
    channel_PLN,
):
    # given
    query = ORDER_LINES_CREATE_MUTATION
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)

    order = order_with_lines
    order.channel = channel_PLN
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status", "channel"])

    variant = variant_with_many_stocks
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    # when
    response = staff_api_client.post_graphql(query, variables)

    # then
    assert_no_permission(response)


@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_by_app(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    order_with_lines,
    permission_manage_orders,
    app_api_client,
    variant_with_many_stocks,
    channel_PLN,
):
    # given
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status"])
    variant = variant_with_many_stocks
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    # when
    response = app_api_client.post_graphql(
        query, variables, permissions=(permission_manage_orders,)
    )

    # then

    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity

    assert OrderEvent.objects.count() == 1
    event = OrderEvent.objects.last()
    assert event.type == order_events.OrderEvents.ADDED_PRODUCTS
    assert len(event.parameters["lines"]) == 1
    line = OrderLine.objects.last()
    assert event.parameters["lines"] == [
        {"item": str(line), "line_pk": str(line.pk), "quantity": quantity}
    ]
    assert_proper_webhook_called_once(
        order,
        OrderStatus.UNCONFIRMED,
        draft_order_updated_webhook_mock,
        order_updated_webhook_mock,
    )


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
def test_order_lines_create_for_just_published_product(
    product_variant_out_of_stock_webhook_mock,
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant_with_many_stocks,
):
    # given
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    variant = variant_with_many_stocks
    product_listing = variant.product.channel_listings.get(channel=order.channel)
    product_listing.published_at = datetime.now(pytz.utc)
    product_listing.save(update_fields=["published_at"])

    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    # when
    response = staff_api_client.post_graphql(query, variables)

    # then
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )
    assert OrderEvent.objects.count() == 1
    assert OrderEvent.objects.last().type == order_events.OrderEvents.ADDED_PRODUCTS
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity


@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_with_unavailable_variant(
    order_updated_webhook_mock,
    draft_order_updated_webhoook_mock,
    draft_order,
    permission_group_manage_orders,
    staff_api_client,
):
    query = ORDER_LINES_CREATE_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = draft_order
    channel = order.channel
    line = order.lines.first()
    variant = line.variant
    variant.channel_listings.filter(channel=channel).update(price_amount=None)
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    error = content["data"]["orderLinesCreate"]["errors"][0]
    assert error["code"] == OrderErrorCode.NOT_AVAILABLE_IN_CHANNEL.name
    assert error["field"] == "input"
    assert error["variants"] == [variant_id]
    order_updated_webhook_mock.assert_not_called()
    draft_order_updated_webhoook_mock.assert_not_called()


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_order_lines_create_when_some_line_has_deleted_product(
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
):
    query = ORDER_LINES_CREATE_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_with_lines
    line = order.lines.first()
    line2 = order.lines.last()
    assert line.variant != line2.variant
    line2.variant = None
    line2.save(update_fields=["variant"])
    order.status = status
    order.save(update_fields=["status"])

    variant = line.variant
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]

    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == line.quantity + quantity


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_with_existing_variant(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
):
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    line = order.lines.first()
    variant = line.variant
    old_quantity = line.quantity
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    # mutation should fail without proper permissions
    response = staff_api_client.post_graphql(query, variables)
    assert_no_permission(response)
    assert not OrderEvent.objects.exists()
    order_updated_webhook_mock.assert_not_called()
    draft_order_updated_webhook_mock.assert_not_called()

    # assign permissions
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(query, variables)
    assert OrderEvent.objects.count() == 1
    assert OrderEvent.objects.last().type == order_events.OrderEvents.ADDED_PRODUCTS
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == old_quantity + quantity
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_with_same_variant_and_force_new_line(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
):
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    lines = order.lines.all()
    assert len(lines) == 2
    line = lines[0]
    variant = line.variant

    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {
        "orderId": order_id,
        "variantId": variant_id,
        "quantity": quantity,
        "forceNewLine": True,
    }

    # mutation should fail without proper permissions
    response = staff_api_client.post_graphql(query, variables)
    assert_no_permission(response)
    assert not OrderEvent.objects.exists()
    order_updated_webhook_mock.assert_not_called()
    draft_order_updated_webhook_mock.assert_not_called()

    # assign permissions
    permission_group_manage_orders.user_set.add(staff_api_client.user)

    response = staff_api_client.post_graphql(query, variables)
    assert order.lines.count() == 3
    assert OrderEvent.objects.count() == 1
    assert OrderEvent.objects.last().type == order_events.OrderEvents.ADDED_PRODUCTS
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_when_variant_already_in_multiple_lines(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
):
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])

    line = order.lines.first()
    variant = line.variant

    # copy line and add to order
    line.id = None
    line.save()

    assert order.lines.count() == 3

    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {
        "orderId": order_id,
        "variantId": variant_id,
        "quantity": quantity,
        "forceNewLine": True,
    }

    # assign permissions
    permission_group_manage_orders.user_set.add(staff_api_client.user)

    response = staff_api_client.post_graphql(ORDER_LINES_CREATE_MUTATION, variables)

    assert order.lines.count() == 4
    assert OrderEvent.objects.count() == 1
    assert OrderEvent.objects.last().type == order_events.OrderEvents.ADDED_PRODUCTS
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_variant_on_promotion(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant_with_many_stocks,
    promotion_without_rules,
    promotion_translation_fr,
    promotion_rule_translation_fr,
):
    # given
    query = ORDER_LINES_CREATE_MUTATION

    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])

    variant = variant_with_many_stocks

    reward_value = Decimal("5")
    rule = promotion_without_rules.rules.create(
        name="Promotion rule",
        catalogue_predicate={
            "productPredicate": {
                "ids": [graphene.Node.to_global_id("Product", variant.product.id)]
            }
        },
        reward_value_type=RewardValueType.FIXED,
        reward_value=reward_value,
    )
    rule.channels.add(order.channel)

    variant_channel_listing = variant.channel_listings.get(channel=order.channel)
    variant_channel_listing.discounted_price_amount = (
        variant_channel_listing.price.amount - reward_value
    )
    variant_channel_listing.save(update_fields=["discounted_price_amount"])

    variant_channel_listing.variantlistingpromotionrule.create(
        promotion_rule=rule,
        discount_amount=reward_value,
        currency=order.channel.currency_code,
    )

    promotion_translation_fr.promotion = promotion_without_rules
    promotion_translation_fr.language_code = order.language_code
    promotion_translation_fr.save(update_fields=["promotion", "language_code"])

    promotion_rule_translation_fr.promotion_rule = rule
    promotion_rule_translation_fr.language_code = order.language_code
    promotion_rule_translation_fr.save(
        update_fields=["promotion_rule", "language_code"]
    )

    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    permission_group_manage_orders.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(query, variables)

    # then
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )
    assert OrderEvent.objects.count() == 1
    assert OrderEvent.objects.last().type == order_events.OrderEvents.ADDED_PRODUCTS
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    line_data = data["orderLines"][0]
    assert line_data["productSku"] == variant.sku
    assert line_data["quantity"] == quantity
    assert line_data["quantity"] == quantity

    assert (
        line_data["unitPrice"]["gross"]["amount"]
        == variant_channel_listing.price_amount - reward_value
    )
    assert (
        line_data["unitPrice"]["net"]["amount"]
        == variant_channel_listing.price_amount - reward_value
    )
    assert line_data["saleId"] == graphene.Node.to_global_id(
        "Promotion", promotion_without_rules.id
    )

    line = order.lines.get(product_sku=variant.sku)
    assert line.sale_id == graphene.Node.to_global_id(
        "Promotion", promotion_without_rules.id
    )
    assert line.unit_discount_amount == reward_value
    assert line.unit_discount_value == reward_value
    assert line.unit_discount_reason == f"Promotion: {line.sale_id}"
    assert line.discounts.count() == 1
    discount = line.discounts.first()
    assert discount.promotion_rule == rule
    assert discount.amount_value == reward_value
    assert discount.type == DiscountType.PROMOTION
    assert discount.name == f"{promotion_without_rules.name}: {rule.name}"
    assert (
        discount.translated_name
        == f"{promotion_translation_fr.name}: {promotion_rule_translation_fr.name}"
    )


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_with_product_and_variant_not_assigned_to_channel(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant,
):
    query = ORDER_LINES_CREATE_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    line = order.lines.first()
    assert variant != line.variant
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": 1}
    variant.product.channel_listings.all().delete()
    variant.channel_listings.all().delete()

    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    error = content["data"]["orderLinesCreate"]["errors"][0]
    assert error["code"] == OrderErrorCode.PRODUCT_NOT_PUBLISHED.name
    assert error["field"] == "input"
    assert error["variants"] == [variant_id]
    order_updated_webhook_mock.assert_not_called()
    draft_order_updated_webhook_mock.assert_not_called()


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_order_lines_create_with_variant_not_assigned_to_channel(
    order_update_webhook_mock,
    draft_order_update_webhook_mock,
    status,
    order_with_lines,
    staff_api_client,
    permission_group_manage_orders,
    customer_user,
    shipping_method,
    variant,
    channel_USD,
    graphql_address_data,
):
    query = ORDER_LINES_CREATE_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    line = order.lines.first()
    assert variant != line.variant
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": 1}
    variant.channel_listings.all().delete()

    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    error = content["data"]["orderLinesCreate"]["errors"][0]
    assert error["code"] == OrderErrorCode.NOT_AVAILABLE_IN_CHANNEL.name
    assert error["field"] == "input"
    assert error["variants"] == [variant_id]
    order_update_webhook_mock.assert_not_called()
    draft_order_update_webhook_mock.assert_not_called()


@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_order_lines_create_without_sku(
    product_variant_out_of_stock_webhook_mock,
    status,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant_with_many_stocks,
):
    ProductVariant.objects.update(sku=None)
    order_with_lines.lines.update(product_sku=None)

    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    variant = variant_with_many_stocks
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": quantity}

    # mutation should fail without proper permissions
    response = staff_api_client.post_graphql(query, variables)
    assert_no_permission(response)
    assert not OrderEvent.objects.exists()

    # assign permissions
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(query, variables)
    assert OrderEvent.objects.count() == 1
    assert OrderEvent.objects.last().type == order_events.OrderEvents.ADDED_PRODUCTS
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] is None
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity

    # mutation should fail when quantity is lower than 1
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": 0}
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["errors"]
    assert data["errors"][0]["field"] == "quantity"
    assert data["errors"][0]["variants"] == [variant_id]
    product_variant_out_of_stock_webhook_mock.assert_not_called()


@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
def test_invalid_order_when_creating_lines(
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    order_with_lines,
    staff_api_client,
    permission_group_manage_orders,
):
    query = ORDER_LINES_CREATE_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_with_lines
    line = order.lines.first()
    variant = line.variant
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    variables = {"orderId": order_id, "variantId": variant_id, "quantity": 1}
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["errors"]
    order_updated_webhook_mock.assert_not_called()
    draft_order_updated_webhook_mock.assert_not_called()


@pytest.mark.parametrize(
    "status,force_new_line",
    [(OrderStatus.DRAFT, False), (OrderStatus.UNCONFIRMED, True)],
)
@patch("saleor.plugins.manager.PluginsManager.draft_order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
def test_order_lines_create_with_custom_price(
    product_variant_out_of_stock_webhook_mock,
    order_updated_webhook_mock,
    draft_order_updated_webhook_mock,
    status,
    force_new_line,
    order_with_lines,
    permission_group_manage_orders,
    staff_api_client,
    variant_with_many_stocks,
):
    # give
    query = ORDER_LINES_CREATE_MUTATION
    order = order_with_lines
    order.status = status
    order.save(update_fields=["status"])
    variant = variant_with_many_stocks
    quantity = 1
    order_id = graphene.Node.to_global_id("Order", order.id)
    variant_id = graphene.Node.to_global_id("ProductVariant", variant.id)
    custom_price = 18
    variables = {
        "orderId": order_id,
        "variantId": variant_id,
        "quantity": quantity,
        "price": custom_price,
        "forceNewLine": force_new_line,
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(query, variables)

    # then
    assert_proper_webhook_called_once(
        order, status, draft_order_updated_webhook_mock, order_updated_webhook_mock
    )
    assert OrderEvent.objects.count() == 1
    event = OrderEvent.objects.last()
    assert event.type == order_events.OrderEvents.ADDED_PRODUCTS
    assert len(event.parameters["lines"]) == 1
    line = OrderLine.objects.last()
    assert line.undiscounted_base_unit_price_amount == custom_price
    assert line.base_unit_price_amount == custom_price
    assert event.parameters["lines"] == [
        {"item": str(line), "line_pk": str(line.pk), "quantity": quantity}
    ]

    content = get_graphql_content(response)
    data = content["data"]["orderLinesCreate"]
    assert data["orderLines"][0]["productSku"] == variant.sku
    assert data["orderLines"][0]["productVariantId"] == variant.get_global_id()
    assert data["orderLines"][0]["quantity"] == quantity
