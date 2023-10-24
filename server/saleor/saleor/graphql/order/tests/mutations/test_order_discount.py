from decimal import Decimal
from functools import partial
from unittest.mock import patch

import graphene
import pytest
from prices import Money, TaxedMoney, fixed_discount, percentage_discount

from .....core.prices import quantize_price
from .....discount import DiscountValueType
from .....order import OrderEvents, OrderStatus
from .....order.error_codes import OrderErrorCode
from .....order.interface import OrderTaxedPricesData
from ....discount.enums import DiscountValueTypeEnum
from ....tests.utils import assert_no_permission, get_graphql_content

ORDER_DISCOUNT_ADD = """
mutation OrderDiscountAdd($orderId: ID!, $input: OrderDiscountCommonInput!){
  orderDiscountAdd(orderId:$orderId, input:$input){
    order{
      lines{
        id
      }
      total{
        gross{
          amount
        }
        net{
          amount
        }
      }
    }
    errors{
      field
      code
      message
    }
  }
}
"""


@pytest.mark.parametrize(
    "value,value_type",
    [
        (Decimal("2222222"), DiscountValueTypeEnum.FIXED.name),
        (Decimal("101"), DiscountValueTypeEnum.PERCENTAGE.name),
    ],
)
def test_add_order_discount_incorrect_values(
    value, value_type, draft_order, staff_api_client, permission_group_manage_orders
):
    variables = {
        "orderId": graphene.Node.to_global_id("Order", draft_order.pk),
        "input": {"valueType": value_type, "value": value},
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountAdd"]

    errors = data["errors"]

    error = data["errors"][0]
    assert error["field"] == "value"
    assert error["code"] == OrderErrorCode.INVALID.name

    assert len(errors) == 1


def test_add_fixed_order_discount_order_is_not_draft(
    order_with_lines, staff_api_client, permission_group_manage_orders
):
    value = Decimal("10")
    variables = {
        "orderId": graphene.Node.to_global_id("Order", order_with_lines.pk),
        "input": {"valueType": DiscountValueTypeEnum.FIXED.name, "value": value},
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountAdd"]

    errors = data["errors"]
    assert len(errors) == 1
    error = data["errors"][0]
    assert error["field"] == "orderId"
    assert error["code"] == OrderErrorCode.CANNOT_DISCOUNT.name


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_add_fixed_order_discount_to_order(
    status, draft_order, staff_api_client, permission_group_manage_orders
):
    order = draft_order
    order.status = status
    order.save(update_fields=["status"])
    total_before_order_discount = order.total
    value = Decimal("10.000")
    variables = {
        "orderId": graphene.Node.to_global_id("Order", order.pk),
        "input": {"valueType": DiscountValueTypeEnum.FIXED.name, "value": value},
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountAdd"]

    order.refresh_from_db()
    expected_net = total_before_order_discount.net.amount - value

    errors = data["errors"]
    assert len(errors) == 0

    # Use `net` values in comparison due to that fixture have taxes incluted in
    # prices but after recalculation taxes are removed because in tests we
    # don't use any tax app.
    assert order.undiscounted_total.net == total_before_order_discount.net
    assert expected_net == order.total.net.amount

    assert order.discounts.count() == 1
    order_discount = order.discounts.first()
    assert order_discount.value == value
    assert order_discount.value_type == DiscountValueType.FIXED
    assert order_discount.amount.amount == value
    assert order_discount.reason is None

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_ADDED
    parameters = event.parameters
    discount_data = parameters.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.FIXED.value
    assert discount_data["amount_value"] == str(order_discount.amount.amount)


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_add_percentage_order_discount_to_order(
    status, draft_order, staff_api_client, permission_group_manage_orders
):
    order = draft_order
    order.status = status
    order.save(update_fields=["status"])
    total_before_order_discount = order.total
    reason = "The reason of the discount"
    value = Decimal("10.000")
    variables = {
        "orderId": graphene.Node.to_global_id("Order", order.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.PERCENTAGE.name,
            "value": value,
            "reason": reason,
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_ADD, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountAdd"]

    order.refresh_from_db()

    discount = partial(percentage_discount, percentage=value)
    expected_net_total = discount(total_before_order_discount.net)
    expected_gross_total = discount(total_before_order_discount.gross)
    expected_total = TaxedMoney(expected_net_total, expected_gross_total)

    errors = data["errors"]
    assert len(errors) == 0

    # Use `net` values in comparison due to that fixture have taxes incluted in
    # prices but after recalculation taxes are removed because in tests we
    # don't use any tax app.
    assert expected_net_total == order.total.net
    assert order.undiscounted_total.net == total_before_order_discount.net

    assert order.discounts.count() == 1
    order_discount = order.discounts.first()
    assert order_discount.value == value
    assert order_discount.value_type == DiscountValueType.PERCENTAGE
    discount_amount = total_before_order_discount.net - expected_total.net
    assert order_discount.amount == discount_amount
    assert order_discount.reason == reason

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_ADDED
    parameters = event.parameters
    discount_data = parameters.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.PERCENTAGE.value
    assert discount_data["amount_value"] == str(order_discount.amount.amount)


def test_add_order_discount_to_order_by_user_no_channel_access(
    draft_order,
    staff_api_client,
    permission_group_all_perms_channel_USD_only,
    channel_PLN,
):
    # given
    order = draft_order
    order.status = OrderStatus.UNCONFIRMED
    order.channel = channel_PLN
    order.save(update_fields=["status", "channel"])
    value = Decimal("10.000")
    variables = {
        "orderId": graphene.Node.to_global_id("Order", order.pk),
        "input": {"valueType": DiscountValueTypeEnum.FIXED.name, "value": value},
    }
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_ADD, variables)

    # then
    assert_no_permission(response)


def test_add_fixed_order_discount_to_order_by_app(
    draft_order, app_api_client, permission_manage_orders
):
    # given
    order = draft_order
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status"])
    total_before_order_discount = order.total
    value = Decimal("10.000")
    variables = {
        "orderId": graphene.Node.to_global_id("Order", order.pk),
        "input": {"valueType": DiscountValueTypeEnum.FIXED.name, "value": value},
    }

    # when
    response = app_api_client.post_graphql(
        ORDER_DISCOUNT_ADD, variables, permissions=(permission_manage_orders,)
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountAdd"]

    order.refresh_from_db()
    expected_net = total_before_order_discount.net.amount - value

    errors = data["errors"]
    assert len(errors) == 0

    # Use `net` values in comparison due to that fixture have taxes incluted in
    # prices but after recalculation taxes are removed because in tests we
    # don't use any tax app.
    assert order.undiscounted_total.net == total_before_order_discount.net
    assert expected_net == order.total.net.amount

    assert order.discounts.count() == 1
    order_discount = order.discounts.first()
    assert order_discount.value == value
    assert order_discount.value_type == DiscountValueType.FIXED
    assert order_discount.amount.amount == value
    assert order_discount.reason is None

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_ADDED
    parameters = event.parameters
    discount_data = parameters.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.FIXED.value
    assert discount_data["amount_value"] == str(order_discount.amount.amount)


ORDER_DISCOUNT_UPDATE = """
mutation OrderDiscountUpdate($discountId: ID!, $input: OrderDiscountCommonInput!){
  orderDiscountUpdate(discountId:$discountId, input: $input){
    order{
      id
      total{
        gross{
          amount
        }
      }
      undiscountedTotal{
        gross{
          amount
        }
      }
    }
    errors{
        field
        message
        code
      }
  }
}
"""


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_update_percentage_order_discount_to_order(
    status,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    order = draft_order_with_fixed_discount_order
    order.status = status
    order.save(update_fields=["status"])
    order_discount = draft_order_with_fixed_discount_order.discounts.get()
    current_undiscounted_total = order.undiscounted_total

    reason = "The reason of the discount"
    value = Decimal("10.000")
    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.PERCENTAGE.name,
            "value": value,
            "reason": reason,
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_UPDATE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountUpdate"]

    order.refresh_from_db()

    discount = partial(percentage_discount, percentage=value)
    expected_net_total = discount(current_undiscounted_total.net)
    expected_gross_total = discount(current_undiscounted_total.gross)
    expected_total = TaxedMoney(expected_net_total, expected_gross_total)

    errors = data["errors"]
    assert len(errors) == 0

    # Use `net` values in comparison due to that fixture have taxes included in
    # prices but after recalculation taxes are removed because in tests we
    # don't use any tax app.
    assert order.undiscounted_total.net == current_undiscounted_total.net
    assert expected_net_total == order.total.net

    assert order.discounts.count() == 1
    order_discount = order.discounts.first()
    assert order_discount.value == value
    assert order_discount.value_type == DiscountValueType.PERCENTAGE
    discount_amount = current_undiscounted_total.net - expected_total.net
    assert order_discount.amount == discount_amount
    assert order_discount.reason == reason

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_UPDATED
    parameters = event.parameters
    discount_data = parameters.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.PERCENTAGE.value
    assert discount_data["amount_value"] == str(discount_amount.amount)


@patch("saleor.order.calculations.PluginsManager.calculate_order_shipping")
@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_update_fixed_order_discount_to_order(
    mocked_function,
    status,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    order = draft_order_with_fixed_discount_order
    mocked_function.return_value = order.shipping_price
    order.status = status
    order.save(update_fields=["status"])
    order_discount = draft_order_with_fixed_discount_order.discounts.get()
    current_undiscounted_total = order.undiscounted_total

    value = Decimal("50.000")
    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.FIXED.name,
            "value": value,
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_UPDATE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountUpdate"]

    order.refresh_from_db()

    discount = partial(fixed_discount, discount=Money(value, currency=order.currency))
    expected_total = discount(current_undiscounted_total)

    errors = data["errors"]
    assert len(errors) == 0

    # Use `net` values in comparison due to that fixture have taxes incluted in
    # prices but after recalculation taxes are removed because in tests we
    # don't use any tax app.
    assert order.undiscounted_total.net == current_undiscounted_total.net
    assert expected_total.net == order.total.net

    assert order.discounts.count() == 1
    order_discount = order.discounts.first()
    assert order_discount.value == value
    assert order_discount.value_type == DiscountValueType.FIXED
    discount_amount = current_undiscounted_total.net - expected_total.net
    assert order_discount.amount == discount_amount

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_UPDATED
    parameters = event.parameters
    discount_data = parameters.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.FIXED.value
    assert discount_data["amount_value"] == str(discount_amount.amount)


def test_update_order_discount_order_is_not_draft(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    draft_order_with_fixed_discount_order.status = OrderStatus.UNFULFILLED
    draft_order_with_fixed_discount_order.save()

    order_discount = draft_order_with_fixed_discount_order.discounts.get()

    value = Decimal("50")
    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.FIXED.name,
            "value": value,
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_UPDATE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountUpdate"]

    errors = data["errors"]
    assert len(errors) == 1

    error = data["errors"][0]
    assert error["field"] == "orderId"
    assert error["code"] == OrderErrorCode.CANNOT_DISCOUNT.name


@pytest.mark.parametrize(
    "value,value_type",
    [
        (Decimal("2222222"), DiscountValueTypeEnum.FIXED.name),
        (Decimal("101"), DiscountValueTypeEnum.PERCENTAGE.name),
    ],
)
def test_update_order_discount_incorrect_values(
    value,
    value_type,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    order_discount = draft_order_with_fixed_discount_order.discounts.get()

    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
        "input": {
            "valueType": value_type,
            "value": value,
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_UPDATE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountUpdate"]

    errors = data["errors"]
    assert len(errors) == 1

    error = errors[0]
    assert error["field"] == "value"
    assert error["code"] == OrderErrorCode.INVALID.name


def test_update_order_discount__by_user_no_channel_access(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_all_perms_channel_USD_only,
    channel_PLN,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.status = OrderStatus.UNCONFIRMED
    order.channel = channel_PLN
    order.save(update_fields=["status", "channel"])
    order_discount = draft_order_with_fixed_discount_order.discounts.get()

    reason = "The reason of the discount"
    value = Decimal("10.000")
    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.PERCENTAGE.name,
            "value": value,
            "reason": reason,
        },
    }
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_UPDATE, variables)

    # then
    assert_no_permission(response)


def test_update_percentage_order_discount_to_order_by_app(
    draft_order_with_fixed_discount_order,
    app_api_client,
    permission_manage_orders,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status"])
    order_discount = draft_order_with_fixed_discount_order.discounts.get()
    current_undiscounted_total = order.undiscounted_total

    reason = "The reason of the discount"
    value = Decimal("10.000")
    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.PERCENTAGE.name,
            "value": value,
            "reason": reason,
        },
    }

    # when
    response = app_api_client.post_graphql(
        ORDER_DISCOUNT_UPDATE, variables, permissions=(permission_manage_orders,)
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountUpdate"]

    order.refresh_from_db()

    discount = partial(percentage_discount, percentage=value)
    expected_net_total = discount(current_undiscounted_total.net)
    expected_gross_total = discount(current_undiscounted_total.gross)
    expected_total = TaxedMoney(expected_net_total, expected_gross_total)

    errors = data["errors"]
    assert len(errors) == 0

    # Use `net` values in comparison due to that fixture have taxes included in
    # prices but after recalculation taxes are removed because in tests we
    # don't use any tax app.
    assert order.undiscounted_total.net == current_undiscounted_total.net
    assert expected_net_total == order.total.net

    assert order.discounts.count() == 1
    order_discount = order.discounts.first()
    assert order_discount.value == value
    assert order_discount.value_type == DiscountValueType.PERCENTAGE
    discount_amount = current_undiscounted_total.net - expected_total.net
    assert order_discount.amount == discount_amount
    assert order_discount.reason == reason

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_UPDATED
    parameters = event.parameters
    discount_data = parameters.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.PERCENTAGE.value
    assert discount_data["amount_value"] == str(discount_amount.amount)


ORDER_DISCOUNT_DELETE = """
mutation OrderDiscountDelete($discountId: ID!){
  orderDiscountDelete(discountId: $discountId){
    order{
      id
    }
    errors{
      field
      message
      code
    }
  }
}
"""


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_delete_order_discount_from_order(
    status,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    order = draft_order_with_fixed_discount_order
    order.status = status
    order.save(update_fields=["status"])

    order_discount = draft_order_with_fixed_discount_order.discounts.get()
    name = "discount translated"
    translated_name = "discount translated name"
    order_discount.name = name
    order_discount.translated_name = translated_name
    order_discount.save(update_fields=["name", "translated_name"])

    current_undiscounted_total = order.undiscounted_total

    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_DELETE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountDelete"]

    order.refresh_from_db()

    errors = data["errors"]
    assert len(errors) == 0

    assert order.undiscounted_total == current_undiscounted_total
    assert order.total == current_undiscounted_total

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_DELETED

    assert order.search_vector


def test_delete_order_discount_order_is_not_draft(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    draft_order_with_fixed_discount_order.status = OrderStatus.UNFULFILLED
    draft_order_with_fixed_discount_order.save()

    order_discount = draft_order_with_fixed_discount_order.discounts.get()

    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_DELETE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountDelete"]

    errors = data["errors"]
    assert len(errors) == 1

    assert draft_order_with_fixed_discount_order.discounts.get()

    error = data["errors"][0]
    assert error["field"] == "orderId"
    assert error["code"] == OrderErrorCode.CANNOT_DISCOUNT.name


def test_delete_order_discount_from_order_by_user_no_channel_access(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_all_perms_channel_USD_only,
    channel_PLN,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.status = OrderStatus.UNCONFIRMED
    order.channel = channel_PLN
    order.save(update_fields=["status", "channel"])

    order_discount = draft_order_with_fixed_discount_order.discounts.get()
    name = "discount translated"
    translated_name = "discount translated name"
    order_discount.name = name
    order_discount.translated_name = translated_name
    order_discount.save(update_fields=["name", "translated_name"])

    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
    }
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(ORDER_DISCOUNT_DELETE, variables)

    # then
    assert_no_permission(response)


def test_delete_order_discount_from_order_by_app(
    draft_order_with_fixed_discount_order,
    app_api_client,
    permission_manage_orders,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status"])

    order_discount = draft_order_with_fixed_discount_order.discounts.get()
    name = "discount translated"
    translated_name = "discount translated name"
    order_discount.name = name
    order_discount.translated_name = translated_name
    order_discount.save(update_fields=["name", "translated_name"])

    current_undiscounted_total = order.undiscounted_total

    variables = {
        "discountId": graphene.Node.to_global_id("OrderDiscount", order_discount.pk),
    }

    # when
    response = app_api_client.post_graphql(
        ORDER_DISCOUNT_DELETE, variables, permissions=(permission_manage_orders,)
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderDiscountDelete"]

    order.refresh_from_db()

    errors = data["errors"]
    assert len(errors) == 0

    assert order.undiscounted_total == current_undiscounted_total
    assert order.total == current_undiscounted_total

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_DISCOUNT_DELETED

    assert order.search_vector


ORDER_LINE_DISCOUNT_UPDATE = """
mutation OrderLineDiscountUpdate($input: OrderDiscountCommonInput!, $orderLineId: ID!){
  orderLineDiscountUpdate(orderLineId: $orderLineId, input: $input){
    orderLine{
      unitPrice{
        gross{
          amount
        }
      }
    }
    errors{
      field
      message
      code
    }
  }
}
"""


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_update_order_line_discount(
    status,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.status = status
    order.save(update_fields=["status"])
    line_to_discount = order.lines.first()
    unit_price = Money(Decimal(7.3), currency="USD")
    line_to_discount.unit_price = TaxedMoney(unit_price, unit_price)
    line_to_discount.undiscounted_unit_price = line_to_discount.unit_price
    line_to_discount.undiscounted_base_unit_price = unit_price
    line_to_discount.base_unit_price = unit_price
    total_price = line_to_discount.unit_price * line_to_discount.quantity
    line_to_discount.total_price = total_price
    line_to_discount.undiscounted_total_price = total_price
    line_to_discount.save()

    line_price_before_discount = line_to_discount.unit_price

    value = Decimal("5")
    reason = "New reason for unit discount"
    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line_to_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.FIXED.name,
            "value": value,
            "reason": reason,
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_UPDATE, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountUpdate"]

    line_to_discount.refresh_from_db()

    errors = data["errors"]
    assert not errors

    discount = partial(
        fixed_discount,
        discount=Money(value, currency=order.currency),
    )
    expected_line_price = discount(line_price_before_discount)

    assert line_to_discount.unit_price == quantize_price(expected_line_price, "USD")
    unit_discount = line_to_discount.unit_discount
    assert unit_discount == (line_price_before_discount - expected_line_price).gross

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_LINE_DISCOUNT_UPDATED
    parameters = event.parameters
    lines = parameters.get("lines", {})
    assert len(lines) == 1

    line_data = lines[0]
    assert line_data.get("line_pk") == str(line_to_discount.pk)
    discount_data = line_data.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.FIXED.value
    assert discount_data["amount_value"] == str(unit_discount.amount)


def test_update_order_line_discount_by_user_no_channel_access(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_all_perms_channel_USD_only,
    channel_PLN,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.channel = channel_PLN
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status", "channel"])
    line_to_discount = order.lines.first()

    value = Decimal("5")
    reason = "New reason for unit discount"
    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line_to_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.FIXED.name,
            "value": value,
            "reason": reason,
        },
    }
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_UPDATE, variables)

    # then
    assert_no_permission(response)


def test_update_order_line_discount_by_app(
    draft_order_with_fixed_discount_order,
    app_api_client,
    permission_manage_orders,
    channel_PLN,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.channel = channel_PLN
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status", "channel"])
    line_to_discount = order.lines.first()

    value = Decimal("5")
    reason = "New reason for unit discount"
    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line_to_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.FIXED.name,
            "value": value,
            "reason": reason,
        },
    }

    # when
    response = app_api_client.post_graphql(
        ORDER_LINE_DISCOUNT_UPDATE, variables, permissions=(permission_manage_orders,)
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountUpdate"]

    line_to_discount.refresh_from_db()

    errors = data["errors"]
    assert not errors

    unit_discount = line_to_discount.unit_discount

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_LINE_DISCOUNT_UPDATED
    parameters = event.parameters
    lines = parameters.get("lines", {})
    assert len(lines) == 1

    line_data = lines[0]
    assert line_data.get("line_pk") == str(line_to_discount.pk)
    discount_data = line_data.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.FIXED.value
    assert discount_data["amount_value"] == str(unit_discount.amount)


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
def test_update_order_line_discount_line_with_discount(
    status,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.status = status
    order.save(update_fields=["status"])
    line_to_discount = order.lines.first()
    unit_price = quantize_price(Money(Decimal(7.3), currency="USD"), currency="USD")
    line_to_discount.base_unit_price = unit_price
    line_to_discount.unit_price = TaxedMoney(unit_price, unit_price)

    line_to_discount.unit_discount_amount = Decimal("2.500")
    line_to_discount.unit_discount_type = DiscountValueType.FIXED
    line_to_discount.unit_discount_value = Decimal("2.500")
    line_to_discount.undiscounted_unit_price_gross_amount = (
        line_to_discount.unit_price_gross_amount + line_to_discount.unit_discount_amount
    )
    line_to_discount.undiscounted_unit_price_net_amount = (
        line_to_discount.unit_price_net_amount + line_to_discount.unit_discount_amount
    )
    line_to_discount.undiscounted_total_price_gross_amount = (
        line_to_discount.undiscounted_unit_price_gross_amount
        * line_to_discount.quantity
    )
    line_to_discount.undiscounted_total_price_net_amount = (
        line_to_discount.undiscounted_unit_price_net_amount * line_to_discount.quantity
    )

    line_to_discount.undiscounted_base_unit_price_amount = (
        unit_price.amount + line_to_discount.unit_discount_amount
    )

    line_to_discount.save()

    line_discount_amount_before_update = line_to_discount.unit_discount_amount
    line_discount_value_before_update = line_to_discount.unit_discount_value

    line_undiscounted_price = line_to_discount.undiscounted_unit_price

    value = Decimal("50")
    reason = "New reason for unit discount"
    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line_to_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.PERCENTAGE.name,
            "value": value,
            "reason": reason,
        },
    }

    permission_group_manage_orders.user_set.add(staff_api_client.user)

    # when
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_UPDATE, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountUpdate"]

    line_to_discount.refresh_from_db()

    errors = data["errors"]
    assert not errors

    discount = partial(
        percentage_discount,
        percentage=value,
    )
    expected_line_price = discount(line_undiscounted_price)

    assert line_to_discount.unit_price == expected_line_price
    unit_discount = line_to_discount.unit_discount
    assert unit_discount == (line_undiscounted_price - expected_line_price).gross

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_LINE_DISCOUNT_UPDATED
    parameters = event.parameters
    lines = parameters.get("lines", {})
    assert len(lines) == 1

    line_data = lines[0]
    assert line_data.get("line_pk") == str(line_to_discount.pk)
    discount_data = line_data.get("discount")

    assert discount_data["value"] == str(value)
    assert discount_data["value_type"] == DiscountValueTypeEnum.PERCENTAGE.value
    assert discount_data["amount_value"] == str(unit_discount.amount)

    assert discount_data["old_value"] == str(line_discount_value_before_update)
    assert discount_data["old_value_type"] == DiscountValueTypeEnum.FIXED.value
    assert discount_data["old_amount_value"] == str(line_discount_amount_before_update)


def test_update_order_line_discount_order_is_not_draft(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    draft_order_with_fixed_discount_order.status = OrderStatus.UNFULFILLED
    draft_order_with_fixed_discount_order.save()

    line_to_discount = draft_order_with_fixed_discount_order.lines.first()

    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line_to_discount.pk),
        "input": {
            "valueType": DiscountValueTypeEnum.FIXED.name,
            "value": Decimal("5"),
            "reason": "New reason for unit discount",
        },
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_UPDATE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountUpdate"]

    line_to_discount.refresh_from_db()

    errors = data["errors"]
    assert len(errors) == 1

    error = data["errors"][0]
    assert error["field"] == "orderId"
    assert error["code"] == OrderErrorCode.CANNOT_DISCOUNT.name

    assert line_to_discount.unit_discount_amount == Decimal("0")


ORDER_LINE_DISCOUNT_REMOVE = """
mutation OrderLineDiscountRemove($orderLineId: ID!){
  orderLineDiscountRemove(orderLineId: $orderLineId){
    orderLine{
      id
    }
    errors{
      field
      message
      code
    }
  }
}
"""


@pytest.mark.parametrize("status", (OrderStatus.DRAFT, OrderStatus.UNCONFIRMED))
@patch("saleor.plugins.manager.PluginsManager.calculate_order_line_unit")
@patch("saleor.plugins.manager.PluginsManager.calculate_order_line_total")
def test_delete_discount_from_order_line(
    mocked_calculate_order_line_total,
    mocked_calculate_order_line_unit,
    status,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    order = draft_order_with_fixed_discount_order
    order.status = status
    order.save(update_fields=["status"])
    line = order.lines.first()

    line_undiscounted_price = TaxedMoney(
        line.undiscounted_base_unit_price, line.undiscounted_base_unit_price
    )
    line_undiscounted_total_price = line_undiscounted_price * line.quantity

    mocked_calculate_order_line_unit.return_value = OrderTaxedPricesData(
        undiscounted_price=line_undiscounted_price,
        price_with_discounts=line_undiscounted_price,
    )
    mocked_calculate_order_line_total.return_value = OrderTaxedPricesData(
        undiscounted_price=line_undiscounted_total_price,
        price_with_discounts=line_undiscounted_total_price,
    )

    line.unit_discount_amount = Decimal("2.5")
    line.unit_discount_type = DiscountValueType.FIXED
    line.unit_discount_value = Decimal("2.5")
    line.save()

    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line.pk),
    }
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_REMOVE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountRemove"]

    errors = data["errors"]
    assert len(errors) == 0

    line.refresh_from_db()

    assert line.unit_price == line_undiscounted_price
    assert line.total_price == line_undiscounted_total_price
    unit_discount = line.unit_discount
    currency = order.currency
    assert unit_discount == Money(Decimal(0), currency=currency)

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_LINE_DISCOUNT_REMOVED
    parameters = event.parameters
    lines = parameters.get("lines", {})
    assert len(lines) == 1

    line_data = lines[0]
    assert line_data.get("line_pk") == str(line.pk)


@patch("saleor.plugins.manager.PluginsManager.calculate_order_line_unit")
@patch("saleor.plugins.manager.PluginsManager.calculate_order_line_total")
def test_delete_discount_from_order_line_by_user_no_channel_access(
    mocked_calculate_order_line_total,
    mocked_calculate_order_line_unit,
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_all_perms_channel_USD_only,
    channel_PLN,
):
    # given
    order = draft_order_with_fixed_discount_order
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)
    order.channel = channel_PLN
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status", "channel"])
    line = order.lines.first()

    line_undiscounted_price = TaxedMoney(
        line.undiscounted_base_unit_price, line.undiscounted_base_unit_price
    )
    line_undiscounted_total_price = line_undiscounted_price * line.quantity

    mocked_calculate_order_line_unit.return_value = OrderTaxedPricesData(
        undiscounted_price=line_undiscounted_price,
        price_with_discounts=line_undiscounted_price,
    )
    mocked_calculate_order_line_total.return_value = OrderTaxedPricesData(
        undiscounted_price=line_undiscounted_total_price,
        price_with_discounts=line_undiscounted_total_price,
    )

    line.unit_discount_amount = Decimal("2.5")
    line.unit_discount_type = DiscountValueType.FIXED
    line.unit_discount_value = Decimal("2.5")
    line.save()

    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line.pk),
    }

    # when
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_REMOVE, variables)

    # then
    assert_no_permission(response)


@patch("saleor.plugins.manager.PluginsManager.calculate_order_line_unit")
@patch("saleor.plugins.manager.PluginsManager.calculate_order_line_total")
def test_delete_discount_from_order_line_by_app(
    mocked_calculate_order_line_total,
    mocked_calculate_order_line_unit,
    draft_order_with_fixed_discount_order,
    app_api_client,
    permission_manage_orders,
    channel_PLN,
):
    # given
    order = draft_order_with_fixed_discount_order
    order.channel = channel_PLN
    order.status = OrderStatus.UNCONFIRMED
    order.save(update_fields=["status", "channel"])
    line = order.lines.first()

    line_undiscounted_price = TaxedMoney(
        line.undiscounted_base_unit_price, line.undiscounted_base_unit_price
    )
    line_undiscounted_total_price = line_undiscounted_price * line.quantity

    mocked_calculate_order_line_unit.return_value = OrderTaxedPricesData(
        undiscounted_price=line_undiscounted_price,
        price_with_discounts=line_undiscounted_price,
    )
    mocked_calculate_order_line_total.return_value = OrderTaxedPricesData(
        undiscounted_price=line_undiscounted_total_price,
        price_with_discounts=line_undiscounted_total_price,
    )

    line.unit_discount_amount = Decimal("2.5")
    line.unit_discount_type = DiscountValueType.FIXED
    line.unit_discount_value = Decimal("2.5")
    line.save()

    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line.pk),
    }

    # when
    response = app_api_client.post_graphql(
        ORDER_LINE_DISCOUNT_REMOVE, variables, permissions=(permission_manage_orders,)
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountRemove"]

    errors = data["errors"]
    assert len(errors) == 0

    line.refresh_from_db()

    assert line.unit_price == line_undiscounted_price
    assert line.total_price == line_undiscounted_total_price
    unit_discount = line.unit_discount
    currency = order.currency
    assert unit_discount == Money(Decimal(0), currency=currency)

    event = order.events.get()
    assert event.type == OrderEvents.ORDER_LINE_DISCOUNT_REMOVED
    parameters = event.parameters
    lines = parameters.get("lines", {})
    assert len(lines) == 1

    line_data = lines[0]
    assert line_data.get("line_pk") == str(line.pk)


def test_delete_order_line_discount_order_is_not_draft(
    draft_order_with_fixed_discount_order,
    staff_api_client,
    permission_group_manage_orders,
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    draft_order_with_fixed_discount_order.status = OrderStatus.UNFULFILLED
    draft_order_with_fixed_discount_order.save()

    line = draft_order_with_fixed_discount_order.lines.first()

    line.unit_discount_amount = Decimal("2.5")
    line.unit_discount_type = DiscountValueType.FIXED
    line.unit_discount_value = Decimal("2.5")
    line.save()

    variables = {
        "orderLineId": graphene.Node.to_global_id("OrderLine", line.pk),
    }
    response = staff_api_client.post_graphql(ORDER_LINE_DISCOUNT_REMOVE, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderLineDiscountRemove"]

    errors = data["errors"]
    assert len(errors) == 1

    assert draft_order_with_fixed_discount_order.discounts.get()

    error = data["errors"][0]
    assert error["field"] == "orderId"
    assert error["code"] == OrderErrorCode.CANNOT_DISCOUNT.name

    assert line.unit_discount_amount == Decimal("2.5")
