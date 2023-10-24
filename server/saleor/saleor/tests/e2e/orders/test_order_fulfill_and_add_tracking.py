import pytest

from .. import DEFAULT_ADDRESS
from ..product.utils.preparing_product import prepare_product
from ..shop.utils import prepare_shop, update_shop_settings
from ..utils import assign_permissions
from .utils import (
    draft_order_complete,
    draft_order_create,
    draft_order_update,
    mark_order_paid,
    order_add_tracking,
    order_fulfill,
    order_lines_create,
    order_query,
)


def prepare_order(e2e_staff_api_client):
    price = 10
    (
        warehouse_id,
        channel_id,
        _channel_slug,
        shipping_method_id,
    ) = prepare_shop(e2e_staff_api_client)

    data = {"fulfillmentAutoApprove": True, "fulfillmentAllowUnpaid": False}
    update_shop_settings(e2e_staff_api_client, data)

    _product_id, product_variant_id, _product_variant_price = prepare_product(
        e2e_staff_api_client,
        warehouse_id,
        channel_id,
        price,
    )

    draft_order_input = {
        "channelId": channel_id,
        "userEmail": "test_user@test.com",
        "shippingAddress": DEFAULT_ADDRESS,
        "billingAddress": DEFAULT_ADDRESS,
    }
    data = draft_order_create(
        e2e_staff_api_client,
        draft_order_input,
    )
    order_id = data["order"]["id"]

    lines = [
        {
            "variantId": product_variant_id,
            "quantity": 1,
        }
    ]
    data = order_lines_create(
        e2e_staff_api_client,
        order_id,
        lines,
    )
    order_line_id = data["order"]["lines"][0]["id"]

    input = {"shippingMethod": shipping_method_id}
    draft_order_update(
        e2e_staff_api_client,
        order_id,
        input,
    )

    return (
        order_id,
        product_variant_id,
        warehouse_id,
        order_line_id,
    )


@pytest.mark.e2e
def test_order_fulfill_and_add_tracking_CORE_0219(
    e2e_staff_api_client,
    permission_manage_products,
    permission_manage_channels,
    permission_manage_product_types_and_attributes,
    permission_manage_shipping,
    permission_manage_orders,
    permission_manage_settings,
):
    # Before
    permissions = [
        permission_manage_products,
        permission_manage_channels,
        permission_manage_shipping,
        permission_manage_product_types_and_attributes,
        permission_manage_orders,
        permission_manage_settings,
    ]
    assign_permissions(e2e_staff_api_client, permissions)

    (
        order_id,
        product_variant_id,
        warehouse_id,
        order_line_id,
    ) = prepare_order(e2e_staff_api_client)

    # Step 1 - Complete the order
    order = draft_order_complete(
        e2e_staff_api_client,
        order_id,
    )
    order_complete_id = order["order"]["id"]
    assert order_complete_id == order_id
    order_line = order["order"]["lines"][0]
    assert order_line["productVariantId"] == product_variant_id
    assert order["order"]["status"] == "UNFULFILLED"

    # Step 2 - Mark order as paid
    order_paid_data = mark_order_paid(
        e2e_staff_api_client,
        order_id,
    )
    assert order_paid_data["order"]["isPaid"] is True
    assert order_paid_data["order"]["paymentStatus"] == "FULLY_CHARGED"
    assert order_paid_data["order"]["status"] == "UNFULFILLED"

    # Step 3 - Fulfill the order and check the status
    input = {
        "lines": [
            {
                "orderLineId": order_line_id,
                "stocks": [
                    {
                        "quantity": 1,
                        "warehouse": warehouse_id,
                    }
                ],
            }
        ],
        "notifyCustomer": True,
        "allowStockToBeExceeded": False,
    }
    order_data = order_fulfill(e2e_staff_api_client, order_id, input)
    fulfillment_id = order_data["order"]["fulfillments"][0]["id"]
    assert order_data["order"]["fulfillments"] != []
    assert order_data["order"]["fulfillments"][0]["status"] == "FULFILLED"

    order = order_query(e2e_staff_api_client, order_id)
    assert order["status"] == "FULFILLED"

    # Step 4 - Add tracking number to the order
    tracking_number = "test"
    data = order_add_tracking(
        e2e_staff_api_client,
        fulfillment_id,
        tracking_number,
    )
    assert data["fulfillments"][0]["trackingNumber"] == tracking_number
