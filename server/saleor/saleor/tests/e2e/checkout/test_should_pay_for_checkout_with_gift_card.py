import pytest

from ..gift_cards.utils import create_gift_card
from ..product.utils.preparing_product import prepare_product
from ..shop.utils.preparing_shop import prepare_shop
from ..utils import assign_permissions
from .utils import (
    checkout_add_promo_code,
    checkout_complete,
    checkout_create,
    checkout_delivery_method_update,
    raw_checkout_dummy_payment_create,
)


@pytest.mark.e2e
def test_pay_for_checkout_with_gift_card_core_1101(
    e2e_logged_api_client,
    e2e_staff_api_client,
    permission_manage_products,
    permission_manage_channels,
    permission_manage_shipping,
    permission_manage_product_types_and_attributes,
    permission_manage_gift_card,
):
    # Before
    permissions = [
        permission_manage_products,
        permission_manage_channels,
        permission_manage_shipping,
        permission_manage_product_types_and_attributes,
        permission_manage_gift_card,
    ]
    assign_permissions(e2e_staff_api_client, permissions)

    (
        warehouse_id,
        channel_id,
        channel_slug,
        shipping_method_id,
    ) = prepare_shop(e2e_staff_api_client)

    (
        _product_id,
        product_variant_id,
        product_variant_price,
    ) = prepare_product(
        e2e_staff_api_client,
        warehouse_id,
        channel_id,
        variant_price=24.99,
    )
    gift_card = create_gift_card(e2e_staff_api_client, 100, "USD", active=True)
    gift_card_code = gift_card["code"]
    gift_card_id = gift_card["id"]

    # Step 1 - Create checkout for product
    lines = [
        {
            "variantId": product_variant_id,
            "quantity": 3,
        },
    ]
    checkout_data = checkout_create(
        e2e_logged_api_client,
        lines,
        channel_slug,
        email="testEmail@example.com",
        set_default_billing_address=True,
        set_default_shipping_address=True,
    )
    checkout_id = checkout_data["id"]
    shipping_method_id = checkout_data["shippingMethods"][0]["id"]
    assert checkout_data["isShippingRequired"] is True
    assert checkout_data["totalPrice"]["gross"]["amount"] == float(
        product_variant_price * 3
    )

    # Step 2 - Set DeliveryMethod for checkout.
    checkout_data = checkout_delivery_method_update(
        e2e_logged_api_client,
        checkout_id,
        shipping_method_id,
    )
    assert checkout_data["deliveryMethod"]["id"] == shipping_method_id
    total_gross_amount = checkout_data["totalPrice"]["gross"]["amount"]
    shipping_price = checkout_data["deliveryMethod"]["price"]["amount"]
    assert shipping_price == 10
    assert total_gross_amount == float(product_variant_price * 3) + shipping_price

    # Step 3 Add gift card to checkout
    checkout_data = checkout_add_promo_code(
        e2e_logged_api_client,
        checkout_id,
        gift_card_code,
    )
    total_gross_amount = checkout_data["totalPrice"]["gross"]["amount"]
    assert total_gross_amount == 0
    assert checkout_data["giftCards"][0]["id"] == gift_card_id
    assert checkout_data["giftCards"][0]["last4CodeChars"] == gift_card_code[-4:]

    # Step 4 - Create payment for checkout.
    create_payment = raw_checkout_dummy_payment_create(
        e2e_logged_api_client,
        checkout_id,
        total_gross_amount,
        token="fully_charged",
    )
    assert create_payment["errors"] == []
    assert create_payment["checkout"]["id"] == checkout_id

    # Step 5 - Complete checkout.
    order_data = checkout_complete(
        e2e_logged_api_client,
        checkout_id,
    )
    assert order_data["status"] == "UNFULFILLED"
    assert order_data["total"]["gross"]["amount"] == 0
    assert order_data["giftCards"][0]["id"] == gift_card_id
    assert order_data["giftCards"][0]["last4CodeChars"] == gift_card_code[-4:]
