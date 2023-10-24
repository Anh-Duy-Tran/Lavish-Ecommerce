from decimal import Decimal
from unittest.mock import patch

import pytest
from prices import Money, TaxedMoney

from ...channel import MarkAsPaidStrategy
from ...giftcard import GiftCardEvents
from ...giftcard.models import GiftCard, GiftCardEvent
from ...order.fetch import OrderLineInfo, fetch_order_info
from ...payment import ChargeStatus, PaymentError, TransactionEventType, TransactionKind
from ...payment.models import Payment
from ...plugins.manager import get_plugins_manager
from ...product.models import DigitalContent
from ...product.tests.utils import create_image
from ...tests.utils import flush_post_commit_hooks
from ...warehouse.models import Allocation, Stock
from .. import (
    FulfillmentStatus,
    OrderAuthorizeStatus,
    OrderChargeStatus,
    OrderEvents,
    OrderStatus,
)
from ..actions import (
    automatically_fulfill_digital_lines,
    cancel_fulfillment,
    cancel_order,
    clean_mark_order_as_paid,
    fulfill_order_lines,
    handle_fully_paid_order,
    mark_order_as_paid_with_payment,
    mark_order_as_paid_with_transaction,
    order_refunded,
    order_transaction_updated,
)
from ..models import Fulfillment, OrderLine
from ..notifications import (
    send_fulfillment_confirmation_to_customer,
    send_payment_confirmation,
)
from ..utils import updates_amounts_for_order


@pytest.fixture
def order_with_digital_line(order, digital_content, stock, site_settings):
    site_settings.automatic_fulfillment_digital_products = True
    site_settings.save()

    variant = stock.product_variant
    variant.digital_content = digital_content
    variant.digital_content.save()

    product_type = variant.product.product_type
    product_type.is_shipping_required = False
    product_type.is_digital = True
    product_type.save()

    quantity = 3
    product = variant.product
    channel = order.channel
    variant_channel_listing = variant.channel_listings.get(channel=channel)
    net = variant.get_price(variant_channel_listing)
    gross = Money(amount=net.amount * Decimal(1.23), currency=net.currency)
    unit_price = TaxedMoney(net=net, gross=gross)
    line = order.lines.create(
        product_name=str(product),
        variant_name=str(variant),
        product_sku=variant.sku,
        product_variant_id=variant.get_global_id(),
        is_shipping_required=variant.is_shipping_required(),
        is_gift_card=variant.is_gift_card(),
        quantity=quantity,
        variant=variant,
        unit_price=unit_price,
        total_price=unit_price * quantity,
        tax_rate=Decimal("0.23"),
    )

    Allocation.objects.create(order_line=line, stock=stock, quantity_allocated=quantity)

    return order


@patch(
    "saleor.order.actions.send_fulfillment_confirmation_to_customer",
    wraps=send_fulfillment_confirmation_to_customer,
)
@patch(
    "saleor.order.actions.send_payment_confirmation", wraps=send_payment_confirmation
)
@patch("saleor.plugins.manager.PluginsManager.fulfillment_created")
def test_handle_fully_paid_order_digital_lines(
    mock_fulfillment_created,
    mock_send_payment_confirmation,
    send_fulfillment_confirmation_to_customer,
    order_with_digital_line,
):
    order = order_with_digital_line
    order.payments.add(Payment.objects.create())
    redirect_url = "http://localhost.pl"
    order = order_with_digital_line
    order.redirect_url = redirect_url
    order.save()
    order_info = fetch_order_info(order)
    manager = get_plugins_manager()

    handle_fully_paid_order(manager, order_info)

    fulfillment = order.fulfillments.first()
    event_order_paid = order.events.get()

    assert event_order_paid.type == OrderEvents.ORDER_FULLY_PAID

    mock_send_payment_confirmation.assert_called_once_with(order_info, manager)
    send_fulfillment_confirmation_to_customer.assert_called_once_with(
        order, fulfillment, user=order.user, app=None, manager=manager
    )

    order.refresh_from_db()
    assert order.status == OrderStatus.FULFILLED
    mock_fulfillment_created.assert_called_once_with(fulfillment)


@patch("saleor.order.actions.send_payment_confirmation")
def test_handle_fully_paid_order(mock_send_payment_confirmation, order):
    manager = get_plugins_manager()

    order.payments.add(Payment.objects.create())
    order_info = fetch_order_info(order)

    handle_fully_paid_order(manager, order_info)

    event_order_paid = order.events.get()
    assert event_order_paid.type == OrderEvents.ORDER_FULLY_PAID

    mock_send_payment_confirmation.assert_called_once_with(order_info, manager)


@patch("saleor.order.notifications.send_payment_confirmation")
def test_handle_fully_paid_order_no_email(mock_send_payment_confirmation, order):
    order.user = None
    order.user_email = ""
    manager = get_plugins_manager()
    order_info = fetch_order_info(order)

    handle_fully_paid_order(manager, order_info)
    event = order.events.get()
    assert event.type == OrderEvents.ORDER_FULLY_PAID
    assert not mock_send_payment_confirmation.called


@patch("saleor.giftcard.utils.send_gift_card_notification")
@patch("saleor.order.actions.send_payment_confirmation")
def test_handle_fully_paid_order_gift_cards_created(
    mock_send_payment_confirmation,
    send_notification_mock,
    site_settings,
    order_with_lines,
    non_shippable_gift_card_product,
    shippable_gift_card_product,
):
    """Ensure the non shippable gift card are fulfilled when the flag for automatic
    fulfillment non shippable gift card is set."""
    # given
    channel = order_with_lines.channel
    channel.automatically_fulfill_non_shippable_gift_card = True
    channel.save()

    order = order_with_lines

    non_shippable_gift_card_line = order_with_lines.lines.first()
    non_shippable_variant = non_shippable_gift_card_product.variants.get()
    non_shippable_gift_card_line.variant = non_shippable_variant
    non_shippable_gift_card_line.is_gift_card = True
    non_shippable_gift_card_line.is_shipping_required = False
    non_shippable_gift_card_line.quantity = 1
    allocation = non_shippable_gift_card_line.allocations.first()
    allocation.quantity_allocated = 1
    allocation.save(update_fields=["quantity_allocated"])

    shippable_gift_card_line = order_with_lines.lines.last()
    shippable_variant = shippable_gift_card_product.variants.get()
    shippable_gift_card_line.variant = shippable_variant
    shippable_gift_card_line.is_gift_card = True
    shippable_gift_card_line.is_shipping_required = True
    shippable_gift_card_line.quantity = 1

    OrderLine.objects.bulk_update(
        [non_shippable_gift_card_line, shippable_gift_card_line],
        ["variant", "is_gift_card", "is_shipping_required", "quantity"],
    )

    manager = get_plugins_manager()

    order.payments.add(Payment.objects.create())
    order_info = fetch_order_info(order)

    # when
    handle_fully_paid_order(manager, order_info)

    # then
    flush_post_commit_hooks()
    assert order.events.filter(type=OrderEvents.ORDER_FULLY_PAID)

    mock_send_payment_confirmation.assert_called_once_with(order_info, manager)

    flush_post_commit_hooks()
    gift_card = GiftCard.objects.get()
    assert gift_card.initial_balance == non_shippable_gift_card_line.unit_price_gross
    assert GiftCardEvent.objects.filter(gift_card=gift_card, type=GiftCardEvents.BOUGHT)

    send_notification_mock.assert_called_once_with(
        None,
        None,
        order.user,
        order.user_email,
        gift_card,
        manager,
        order.channel.slug,
        resending=False,
    )


@patch("saleor.giftcard.utils.send_gift_card_notification")
@patch("saleor.order.actions.send_payment_confirmation")
def test_handle_fully_paid_order_gift_cards_not_created(
    mock_send_payment_confirmation,
    send_notification_mock,
    site_settings,
    order_with_lines,
    non_shippable_gift_card_product,
    shippable_gift_card_product,
):
    """Ensure the non shippable gift card are not fulfilled when the flag for
    automatic fulfillment non shippable gift card is not set."""
    # given
    channel = order_with_lines.channel
    channel.automatically_fulfill_non_shippable_gift_card = False
    channel.save()

    order = order_with_lines

    non_shippable_gift_card_line = order_with_lines.lines.first()
    non_shippable_variant = non_shippable_gift_card_product.variants.get()
    non_shippable_gift_card_line.variant = non_shippable_variant
    non_shippable_gift_card_line.is_gift_card = True
    non_shippable_gift_card_line.is_shipping_required = False
    non_shippable_gift_card_line.quantity = 1
    allocation = non_shippable_gift_card_line.allocations.first()
    allocation.quantity_allocated = 1
    allocation.save(update_fields=["quantity_allocated"])

    shippable_gift_card_line = order_with_lines.lines.last()
    shippable_variant = shippable_gift_card_product.variants.get()
    shippable_gift_card_line.variant = shippable_variant
    shippable_gift_card_line.is_gift_card = True
    shippable_gift_card_line.is_shipping_required = True
    shippable_gift_card_line.quantity = 1

    OrderLine.objects.bulk_update(
        [non_shippable_gift_card_line, shippable_gift_card_line],
        ["variant", "is_gift_card", "is_shipping_required", "quantity"],
    )

    manager = get_plugins_manager()

    order.payments.add(Payment.objects.create())
    order_info = fetch_order_info(order)

    # when
    handle_fully_paid_order(manager, order_info)

    # then
    flush_post_commit_hooks()
    assert order.events.filter(type=OrderEvents.ORDER_FULLY_PAID)

    mock_send_payment_confirmation.assert_called_once_with(order_info, manager)

    flush_post_commit_hooks()
    assert not GiftCard.objects.exists()
    send_notification_mock.assert_not_called


def test_mark_as_paid_with_payment(admin_user, draft_order):
    manager = get_plugins_manager()
    mark_order_as_paid_with_payment(draft_order, admin_user, None, manager)
    payment = draft_order.payments.last()
    assert payment.charge_status == ChargeStatus.FULLY_CHARGED
    assert payment.captured_amount == draft_order.total.gross.amount
    assert draft_order.events.last().type == (OrderEvents.ORDER_MARKED_AS_PAID)
    transactions = payment.transactions.all()
    assert transactions.count() == 1
    assert transactions[0].kind == TransactionKind.EXTERNAL


def test_mark_as_paid_with_external_reference_with_payment(admin_user, draft_order):
    external_reference = "transaction_id"
    manager = get_plugins_manager()
    mark_order_as_paid_with_payment(
        draft_order, admin_user, None, manager, external_reference=external_reference
    )
    payment = draft_order.payments.last()
    assert payment.charge_status == ChargeStatus.FULLY_CHARGED
    assert payment.captured_amount == draft_order.total.gross.amount
    assert payment.psp_reference == external_reference
    assert draft_order.events.last().type == (OrderEvents.ORDER_MARKED_AS_PAID)
    transactions = payment.transactions.all()
    assert transactions.count() == 1
    assert transactions[0].kind == TransactionKind.EXTERNAL
    assert transactions[0].token == external_reference


def test_mark_as_paid_no_billing_address(admin_user, draft_order):
    draft_order.billing_address = None
    draft_order.save()

    manager = get_plugins_manager()
    with pytest.raises(Exception):
        mark_order_as_paid_with_payment(draft_order, admin_user, None, manager)


def test_clean_mark_order_as_paid(payment_txn_preauth):
    order = payment_txn_preauth.order
    with pytest.raises(PaymentError):
        clean_mark_order_as_paid(order)


def test_mark_as_paid_with_transaction(admin_user, draft_order):
    # given
    manager = get_plugins_manager()
    channel = draft_order.channel
    channel.order_mark_as_paid_strategy = MarkAsPaidStrategy.TRANSACTION_FLOW
    channel.save(update_fields=["order_mark_as_paid_strategy"])

    # when
    mark_order_as_paid_with_transaction(draft_order, admin_user, None, manager)

    # then
    draft_order.refresh_from_db()
    assert not draft_order.payments.exists()
    transaction = draft_order.payment_transactions.get()

    assert transaction.charged_value == draft_order.total.gross.amount
    assert draft_order.authorize_status == OrderAuthorizeStatus.FULL
    assert draft_order.charge_status == OrderChargeStatus.FULL
    assert draft_order.total_charged.amount == transaction.charged_value

    transaction_event = transaction.events.filter(
        type=TransactionEventType.CHARGE_SUCCESS
    ).get()
    assert transaction_event.amount_value == draft_order.total.gross.amount
    assert transaction_event.type == TransactionEventType.CHARGE_SUCCESS


def test_mark_as_paid_with_external_reference_with_transaction(admin_user, draft_order):
    # given
    external_reference = "transaction_id"
    manager = get_plugins_manager()
    channel = draft_order.channel
    channel.order_mark_as_paid_strategy = MarkAsPaidStrategy.TRANSACTION_FLOW
    channel.save(update_fields=["order_mark_as_paid_strategy"])

    # when
    mark_order_as_paid_with_transaction(
        draft_order, admin_user, None, manager, external_reference=external_reference
    )

    # then
    assert not draft_order.payments.exists()
    transaction = draft_order.payment_transactions.get()
    assert transaction.psp_reference == external_reference


def test_cancel_fulfillment(fulfilled_order, warehouse):
    fulfillment = fulfilled_order.fulfillments.first()
    line_1, line_2 = fulfillment.lines.all()

    cancel_fulfillment(fulfillment, None, None, warehouse, get_plugins_manager())

    fulfillment.refresh_from_db()
    fulfilled_order.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.CANCELED
    assert fulfilled_order.status == OrderStatus.UNFULFILLED
    assert line_1.order_line.quantity_fulfilled == 0
    assert line_2.order_line.quantity_fulfilled == 0


def test_cancel_fulfillment_variant_witout_inventory_tracking(
    fulfilled_order_without_inventory_tracking, warehouse
):
    fulfillment = fulfilled_order_without_inventory_tracking.fulfillments.first()
    line = fulfillment.lines.first()
    stock = line.order_line.variant.stocks.get()
    stock_quantity_before = stock.quantity

    cancel_fulfillment(fulfillment, None, None, warehouse, get_plugins_manager())

    fulfillment.refresh_from_db()
    line.refresh_from_db()
    fulfilled_order_without_inventory_tracking.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.CANCELED
    assert line.order_line.quantity_fulfilled == 0
    assert fulfilled_order_without_inventory_tracking.status == OrderStatus.UNFULFILLED
    assert stock_quantity_before == line.order_line.variant.stocks.get().quantity


@patch("saleor.order.actions.send_order_canceled_confirmation")
def test_cancel_order(
    send_order_canceled_confirmation_mock,
    fulfilled_order_with_all_cancelled_fulfillments,
):
    # given
    order = fulfilled_order_with_all_cancelled_fulfillments
    manager = get_plugins_manager()

    assert Allocation.objects.filter(
        order_line__order=order, quantity_allocated__gt=0
    ).exists()

    # when
    cancel_order(order, None, None, manager)

    # then
    order_event = order.events.last()
    assert order_event.type == OrderEvents.CANCELED

    assert order.status == OrderStatus.CANCELED
    assert not Allocation.objects.filter(
        order_line__order=order, quantity_allocated__gt=0
    ).exists()

    flush_post_commit_hooks()
    send_order_canceled_confirmation_mock.assert_called_once_with(
        order, None, None, manager
    )


@patch("saleor.plugins.manager.PluginsManager.order_refunded")
@patch("saleor.plugins.manager.PluginsManager.order_fully_refunded")
@patch("saleor.order.actions.send_order_refunded_confirmation")
def test_order_refunded_by_user(
    send_order_refunded_confirmation_mock,
    order_fully_refunded_mock,
    order_refunded_mock,
    order,
    checkout_with_item,
):
    # given
    payment = Payment.objects.create(
        gateway="mirumee.payments.dummy", is_active=True, checkout=checkout_with_item
    )
    amount = order.total.gross.amount
    app = None

    # when
    manager = get_plugins_manager()
    order_refunded(order, order.user, app, amount, payment, manager)

    # then
    flush_post_commit_hooks()
    order_event = order.events.last()
    assert order_event.type == OrderEvents.PAYMENT_REFUNDED

    send_order_refunded_confirmation_mock.assert_called_once_with(
        order, order.user, None, amount, order.currency, manager
    )
    order_fully_refunded_mock.assert_called_once_with(order)
    order_refunded_mock.assert_called_once_with(order)


@patch("saleor.plugins.manager.PluginsManager.order_refunded")
@patch("saleor.plugins.manager.PluginsManager.order_fully_refunded")
@patch("saleor.order.actions.send_order_refunded_confirmation")
def test_order_refunded_by_app(
    send_order_refunded_confirmation_mock,
    order_fully_refunded_mock,
    order_refunded_mock,
    order,
    checkout_with_item,
    app,
):
    # given
    payment = Payment.objects.create(
        gateway="mirumee.payments.dummy", is_active=True, checkout=checkout_with_item
    )
    amount = order.total.gross.amount

    # when
    manager = get_plugins_manager()
    order_refunded(order, None, app, amount, payment, manager)

    # then
    flush_post_commit_hooks()
    order_event = order.events.last()
    assert order_event.type == OrderEvents.PAYMENT_REFUNDED

    send_order_refunded_confirmation_mock.assert_called_once_with(
        order, None, app, amount, order.currency, manager
    )
    order_fully_refunded_mock.assert_called_once_with(order)
    order_refunded_mock.assert_called_once_with(order)


def test_fulfill_order_lines(order_with_lines):
    order = order_with_lines
    line = order.lines.first()
    quantity_fulfilled_before = line.quantity_fulfilled
    variant = line.variant
    stock = Stock.objects.get(product_variant=variant)
    stock_quantity_after = stock.quantity - line.quantity

    fulfill_order_lines(
        [
            OrderLineInfo(
                line=line,
                quantity=line.quantity,
                variant=variant,
                warehouse_pk=stock.warehouse.pk,
            )
        ],
        get_plugins_manager(),
    )

    stock.refresh_from_db()
    assert stock.quantity == stock_quantity_after
    assert line.quantity_fulfilled == quantity_fulfilled_before + line.quantity


def test_fulfill_order_lines_multiple_lines(order_with_lines):
    order = order_with_lines
    lines = order.lines.all()

    assert lines.count() > 1

    quantity_fulfilled_before_1 = lines[0].quantity_fulfilled
    variant_1 = lines[0].variant
    stock_1 = Stock.objects.get(product_variant=variant_1)
    stock_quantity_after_1 = stock_1.quantity - lines[0].quantity

    quantity_fulfilled_before_2 = lines[1].quantity_fulfilled
    variant_2 = lines[1].variant
    stock_2 = Stock.objects.get(product_variant=variant_2)
    stock_quantity_after_2 = stock_2.quantity - lines[1].quantity

    fulfill_order_lines(
        [
            OrderLineInfo(
                line=lines[0],
                quantity=lines[0].quantity,
                variant=variant_1,
                warehouse_pk=stock_1.warehouse.pk,
            ),
            OrderLineInfo(
                line=lines[1],
                quantity=lines[1].quantity,
                variant=variant_2,
                warehouse_pk=stock_2.warehouse.pk,
            ),
        ],
        get_plugins_manager(),
    )

    stock_1.refresh_from_db()
    assert stock_1.quantity == stock_quantity_after_1
    assert (
        lines[0].quantity_fulfilled == quantity_fulfilled_before_1 + lines[0].quantity
    )

    stock_2.refresh_from_db()
    assert stock_2.quantity == stock_quantity_after_2
    assert (
        lines[1].quantity_fulfilled == quantity_fulfilled_before_2 + lines[1].quantity
    )


def test_fulfill_order_lines_with_variant_deleted(order_with_lines):
    line = order_with_lines.lines.first()
    line.variant.delete()

    line.refresh_from_db()

    fulfill_order_lines(
        [OrderLineInfo(line=line, quantity=line.quantity)], get_plugins_manager()
    )


def test_fulfill_order_lines_without_inventory_tracking(order_with_lines):
    order = order_with_lines
    line = order.lines.first()
    quantity_fulfilled_before = line.quantity_fulfilled
    variant = line.variant
    variant.track_inventory = False
    variant.save()
    stock = Stock.objects.get(product_variant=variant)

    # stock should not change
    stock_quantity_after = stock.quantity

    fulfill_order_lines(
        [
            OrderLineInfo(
                line=line,
                quantity=line.quantity,
                variant=variant,
                warehouse_pk=stock.warehouse.pk,
            )
        ],
        get_plugins_manager(),
    )

    stock.refresh_from_db()
    assert stock.quantity == stock_quantity_after
    assert line.quantity_fulfilled == quantity_fulfilled_before + line.quantity


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer")
@patch("saleor.order.utils.get_default_digital_content_settings")
@patch("saleor.plugins.manager.PluginsManager.fulfillment_created")
def test_fulfill_digital_lines(
    mock_fulfillment_created,
    mock_digital_settings,
    mock_email_fulfillment,
    order_with_lines,
    media_root,
):
    mock_digital_settings.return_value = {"automatic_fulfillment": True}
    line = order_with_lines.lines.all()[0]

    image_file, image_name = create_image()
    variant = line.variant

    product_type = variant.product.product_type
    product_type.is_digital = True
    product_type.is_shipping_required = False
    product_type.save(update_fields=["is_digital", "is_shipping_required"])

    digital_content = DigitalContent.objects.create(
        content_file=image_file, product_variant=variant, use_default_settings=True
    )

    line.variant.digital_content = digital_content
    line.is_shipping_required = False
    line.save()

    order_with_lines.refresh_from_db()
    order_info = fetch_order_info(order_with_lines)
    manager = get_plugins_manager()

    automatically_fulfill_digital_lines(order_info, manager)

    line.refresh_from_db()
    fulfillment = Fulfillment.objects.get(order=order_with_lines)
    fulfillment_lines = fulfillment.lines.all()

    assert fulfillment_lines.count() == 1
    assert line.digital_content_url
    assert mock_email_fulfillment.called
    mock_fulfillment_created.assert_called_once_with(fulfillment)


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer")
@patch("saleor.order.utils.get_default_digital_content_settings")
@patch("saleor.plugins.manager.PluginsManager.fulfillment_created")
def test_fulfill_digital_lines_no_allocation(
    mock_fulfillment_created,
    mock_digital_settings,
    mock_email_fulfillment,
    order_with_lines,
    media_root,
):
    # given
    mock_digital_settings.return_value = {"automatic_fulfillment": True}
    line = order_with_lines.lines.all()[0]

    image_file, image_name = create_image()
    variant = line.variant

    product_type = variant.product.product_type
    product_type.is_digital = True
    product_type.is_shipping_required = False
    product_type.save(update_fields=["is_digital", "is_shipping_required"])

    digital_content = DigitalContent.objects.create(
        content_file=image_file, product_variant=variant, use_default_settings=True
    )

    variant.digital_content = digital_content
    variant.track_inventory = False
    variant.save()

    line.is_shipping_required = False
    line.allocations.all().delete()
    line.save()

    order_with_lines.refresh_from_db()
    order_info = fetch_order_info(order_with_lines)
    manager = get_plugins_manager()

    # when
    automatically_fulfill_digital_lines(order_info, manager)

    # then
    line.refresh_from_db()
    fulfillment = Fulfillment.objects.get(order=order_with_lines)
    fulfillment_lines = fulfillment.lines.all()

    assert fulfillment_lines.count() == 1
    assert line.digital_content_url
    assert mock_email_fulfillment.called
    mock_fulfillment_created.assert_called_once_with(fulfillment)


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_order_fully_paid(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, charged_value=order_with_lines.total.gross.amount
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    order_fully_paid.assert_called_once_with(order_with_lines)
    order_updated.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_order_partially_paid(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, charged_value=Decimal("10")
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_paid.called
    order_updated.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_order_partially_paid_and_multiple_transactions(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item_generator(
        order_id=order_with_lines.pk, charged_value=Decimal("10")
    )
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, charged_value=Decimal("5")
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_paid.called
    order_updated.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_with_the_same_transaction_charged_amount(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    charged_value = Decimal("5")

    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, charged_value=charged_value
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=charged_value,
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_paid.called
    assert not order_updated.called


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_order_authorized(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk,
        authorized_value=order_with_lines.total.gross.amount,
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_paid.called
    order_updated.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_order_partially_authorized_and_multiple_transactions(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item_generator(
        order_id=order_with_lines.pk, authorized_value=Decimal("10")
    )
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, authorized_value=Decimal("5")
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_paid.called
    order_updated.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_updated")
@patch("saleor.plugins.manager.PluginsManager.order_fully_paid")
def test_order_transaction_updated_with_the_same_transaction_authorized_amount(
    order_fully_paid, order_updated, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    authorized_value = Decimal("5")

    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, authorized_value=authorized_value
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=authorized_value,
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_paid.called
    assert not order_updated.called


@patch("saleor.plugins.manager.PluginsManager.order_refunded")
@patch("saleor.plugins.manager.PluginsManager.order_fully_refunded")
def test_order_transaction_updated_order_fully_refunded(
    order_fully_refunded, order_refunded, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, refunded_value=order_with_lines.total.gross.amount
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    order_fully_refunded.assert_called_once_with(order_with_lines)
    order_refunded.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_refunded")
@patch("saleor.plugins.manager.PluginsManager.order_fully_refunded")
def test_order_transaction_updated_order_partially_refunded(
    order_fully_refunded, order_refunded, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk, refunded_value=Decimal(10)
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    assert not order_fully_refunded.called
    order_refunded.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_refunded")
@patch("saleor.plugins.manager.PluginsManager.order_fully_refunded")
def test_order_transaction_updated_order_fully_refunded_and_multiple_transactions(
    order_fully_refunded, order_refunded, order_with_lines, transaction_item_generator
):
    # given
    order_info = fetch_order_info(order_with_lines)
    transaction_item_generator(
        order_id=order_with_lines.pk, refunded_value=Decimal("10")
    )
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk,
        refunded_value=order_with_lines.total.gross.amount - Decimal("10"),
    )
    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    order_fully_refunded.assert_called_once_with(order_with_lines)
    order_refunded.assert_called_once_with(order_with_lines)


@patch("saleor.plugins.manager.PluginsManager.order_refunded")
@patch("saleor.plugins.manager.PluginsManager.order_fully_refunded")
def test_order_transaction_updated_order_fully_refunded_with_transaction_and_payment(
    order_fully_refunded,
    order_refunded,
    order_with_lines,
    transaction_item_generator,
    payment_dummy,
):
    # given
    payment = payment_dummy
    payment.order = order_with_lines
    payment.charge_status = ChargeStatus.PARTIALLY_REFUNDED
    payment.is_active = True
    payment.save()

    payment.transactions.create(
        amount=Decimal("10"),
        currency=payment.currency,
        kind=TransactionKind.REFUND,
        gateway_response={},
        is_success=True,
    )

    order_info = fetch_order_info(order_with_lines)
    transaction_item = transaction_item_generator(
        order_id=order_with_lines.pk,
        refunded_value=order_with_lines.total.gross.amount - Decimal("10"),
    )

    manager = get_plugins_manager()
    updates_amounts_for_order(
        order_with_lines,
    )

    # when
    order_transaction_updated(
        order_info=order_info,
        transaction_item=transaction_item,
        manager=manager,
        user=None,
        app=None,
        previous_authorized_value=Decimal(0),
        previous_charged_value=Decimal(0),
        previous_refunded_value=Decimal(0),
    )

    # then
    flush_post_commit_hooks()
    order_refunded.assert_called_once_with(order_with_lines)
    order_fully_refunded.assert_called_once_with(order_with_lines)
