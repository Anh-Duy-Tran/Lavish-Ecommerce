import pytest

from ..product.utils.preparing_product import prepare_product
from ..sales.utils import create_sale, create_sale_channel_listing, sale_catalogues_add
from ..shop.utils.preparing_shop import prepare_shop
from ..utils import assign_permissions
from .utils import (
    checkout_complete,
    checkout_create,
    checkout_delivery_method_update,
    checkout_dummy_payment_create,
)


def prepare_sale_for_product(
    e2e_staff_api_client,
    channel_id,
    product_id,
    sale_discount_type,
    sale_discount_value,
):
    sale_name = "Sale"
    sale = create_sale(
        e2e_staff_api_client,
        sale_name,
        sale_discount_type,
    )
    sale_id = sale["id"]
    sale_listing_input = [
        {
            "channelId": channel_id,
            "discountValue": sale_discount_value,
        }
    ]
    create_sale_channel_listing(
        e2e_staff_api_client,
        sale_id,
        add_channels=sale_listing_input,
    )
    catalogue_input = {"products": [product_id]}
    sale_catalogues_add(
        e2e_staff_api_client,
        sale_id,
        catalogue_input,
    )

    return sale_id, sale_discount_value


@pytest.mark.e2e
def test_checkout_products_on_percentage_sale_core_1004(
    e2e_not_logged_api_client,
    e2e_staff_api_client,
    permission_manage_products,
    permission_manage_channels,
    permission_manage_shipping,
    permission_manage_product_types_and_attributes,
    permission_manage_discounts,
):
    # Before
    permissions = [
        permission_manage_products,
        permission_manage_channels,
        permission_manage_shipping,
        permission_manage_product_types_and_attributes,
        permission_manage_discounts,
    ]
    assign_permissions(e2e_staff_api_client, permissions)

    (
        warehouse_id,
        channel_id,
        channel_slug,
        shipping_method_id,
    ) = prepare_shop(e2e_staff_api_client)

    (
        product_id,
        product_variant_id,
        product_variant_price,
    ) = prepare_product(
        e2e_staff_api_client,
        warehouse_id,
        channel_id,
        variant_price="13.33",
    )

    sale_id, sale_discount_value = prepare_sale_for_product(
        e2e_staff_api_client,
        channel_id,
        product_id,
        sale_discount_type="PERCENTAGE",
        sale_discount_value=3,
    )

    # Step 1 - checkoutCreate for product on sale
    lines = [
        {
            "variantId": product_variant_id,
            "quantity": 2,
        },
    ]
    checkout_data = checkout_create(
        e2e_not_logged_api_client,
        lines,
        channel_slug,
        email="testEmail@example.com",
        set_default_billing_address=True,
        set_default_shipping_address=True,
    )
    checkout_id = checkout_data["id"]
    checkout_lines = checkout_data["lines"][0]
    shipping_method_id = checkout_data["shippingMethods"][0]["id"]
    line_discount = round(float(product_variant_price) * sale_discount_value / 100, 2)
    unit_price = float(product_variant_price) - line_discount

    assert checkout_data["isShippingRequired"] is True
    assert checkout_lines["unitPrice"]["gross"]["amount"] == unit_price
    assert checkout_lines["undiscountedUnitPrice"]["amount"] == float(
        product_variant_price
    )

    # Step 2 - Set DeliveryMethod for checkout.
    checkout_data = checkout_delivery_method_update(
        e2e_not_logged_api_client,
        checkout_id,
        shipping_method_id,
    )
    assert checkout_data["deliveryMethod"]["id"] == shipping_method_id
    total_gross_amount = checkout_data["totalPrice"]["gross"]["amount"]
    subtotal_gross_amount = checkout_data["subtotalPrice"]["gross"]["amount"]

    # Step 3 - Create payment for checkout.
    checkout_dummy_payment_create(
        e2e_not_logged_api_client,
        checkout_id,
        total_gross_amount,
    )

    # Step 5 - Complete checkout.
    order_data = checkout_complete(
        e2e_not_logged_api_client,
        checkout_id,
    )
    assert order_data["status"] == "UNFULFILLED"
    assert order_data["total"]["gross"]["amount"] == total_gross_amount
    assert order_data["subtotal"]["gross"]["amount"] == subtotal_gross_amount

    order_line = order_data["lines"][0]
    assert order_line["undiscountedUnitPrice"]["gross"]["amount"] == float(
        product_variant_price
    )
    assert order_line["unitDiscountType"] == "FIXED"
    assert order_line["unitPrice"]["gross"]["amount"] == unit_price
    assert order_line["unitDiscount"]["amount"] == line_discount
    assert order_line["unitDiscountReason"] == f"Sale: {sale_id}"
