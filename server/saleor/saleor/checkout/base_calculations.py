"""Contains functions which are base for calculating checkout properties.

It's recommended to use functions from calculations.py module to take in account
plugin manager. Functions from this module return price without
taxes (Money instead of TaxedMoney). If you don't need pre-taxed prices use functions
from calculations.py.
"""

from typing import TYPE_CHECKING, Iterable, Optional

from prices import Money

from ..core.prices import quantize_price
from ..core.taxes import zero_money
from ..discount import DiscountValueType, VoucherType

if TYPE_CHECKING:
    from ..channel.models import Channel
    from .fetch import CheckoutInfo, CheckoutLineInfo, ShippingMethodInfo


def calculate_base_line_unit_price(
    line_info: "CheckoutLineInfo",
    channel: "Channel",
) -> Money:
    """Calculate line unit price including discounts and vouchers.

    The price includes sales, specific product and applied once per order
    voucher discounts.
    The price does not include the entire order discount.
    """
    total_line_price = calculate_base_line_total_price(
        line_info=line_info, channel=channel
    )
    quantity = line_info.line.quantity
    currency = total_line_price.currency
    return quantize_price(total_line_price / quantity, currency)


def calculate_base_line_total_price(
    line_info: "CheckoutLineInfo",
    channel: "Channel",
) -> Money:
    """Calculate line total price including discounts and vouchers.

    The price includes sales, specific product and applied once per order
    voucher discounts.
    The price does not include the entire order discount.
    """
    variant = line_info.variant
    currency = line_info.channel_listing.currency
    quantity = line_info.line.quantity

    variant_price = variant.get_base_price(
        line_info.channel_listing, line_info.line.price_override
    )

    total_price = variant_price * line_info.line.quantity

    for discount in line_info.discounts:
        discount_amount = Money(discount.amount_value, line_info.line.currency)
        total_price -= discount_amount

    if line_info.voucher:
        if not line_info.voucher.apply_once_per_order:
            if line_info.voucher.discount_value_type == DiscountValueType.PERCENTAGE:
                voucher_discount_amount = line_info.voucher.get_discount_amount_for(
                    total_price, channel=channel
                )
                total_price = max(
                    total_price - voucher_discount_amount, zero_money(currency)
                )
            else:
                unit_price = total_price / quantity
                voucher_unit_discount_amount = (
                    line_info.voucher.get_discount_amount_for(
                        unit_price, channel=channel
                    )
                )
                total_price = max(
                    total_price - (voucher_unit_discount_amount * quantity),
                    zero_money(currency),
                )
        else:
            unit_price = total_price / quantity
            voucher_unit_discount_amount = line_info.voucher.get_discount_amount_for(
                unit_price, channel=channel
            )
            variant_price_with_discounts = max(
                unit_price - voucher_unit_discount_amount, zero_money(currency)
            )
            # we add -1 as we handle a case when voucher is applied only to single line
            # of the cheapest item
            quantity_without_voucher = line_info.line.quantity - 1
            total_price = (
                unit_price * quantity_without_voucher + variant_price_with_discounts
            )

    return quantize_price(total_price, total_price.currency)


def calculate_undiscounted_base_line_total_price(
    line_info: "CheckoutLineInfo",
    channel: "Channel",
) -> Money:
    """Calculate line total price excluding discounts and vouchers."""
    unit_price = calculate_undiscounted_base_line_unit_price(
        line_info=line_info, channel=channel
    )
    total_price = unit_price * line_info.line.quantity
    return quantize_price(total_price, total_price.currency)


def calculate_undiscounted_base_line_unit_price(
    line_info: "CheckoutLineInfo",
    channel: "Channel",
):
    """Calculate line unit price without including discounts and vouchers."""
    variant = line_info.variant
    variant_price = variant.get_base_price(
        line_info.channel_listing, line_info.line.price_override
    )
    return quantize_price(variant_price, variant_price.currency)


def base_checkout_delivery_price(
    checkout_info: "CheckoutInfo",
    lines: Optional[Iterable["CheckoutLineInfo"]] = None,
) -> Money:
    """Calculate base (untaxed) price for any kind of delivery method."""
    currency = checkout_info.checkout.currency

    shipping_price = base_checkout_undiscounted_delivery_price(checkout_info, lines)

    is_shipping_voucher = (
        checkout_info.voucher.type == VoucherType.SHIPPING
        if checkout_info.voucher
        else False
    )

    if is_shipping_voucher:
        discount = checkout_info.checkout.discount
        shipping_price = max(zero_money(currency), shipping_price - discount)

    return quantize_price(
        shipping_price,
        currency,
    )


def base_checkout_undiscounted_delivery_price(
    checkout_info: "CheckoutInfo",
    lines: Optional[Iterable["CheckoutLineInfo"]] = None,
) -> Money:
    """Calculate base (untaxed) undiscounted price for any kind of delivery method."""
    from .fetch import ShippingMethodInfo

    delivery_method_info = checkout_info.delivery_method_info
    currency = checkout_info.checkout.currency

    if not isinstance(delivery_method_info, ShippingMethodInfo):
        return zero_money(currency)

    return calculate_base_price_for_shipping_method(
        checkout_info, delivery_method_info, lines
    )


def calculate_base_price_for_shipping_method(
    checkout_info: "CheckoutInfo",
    shipping_method_info: "ShippingMethodInfo",
    lines: Optional[Iterable["CheckoutLineInfo"]] = None,
) -> Money:
    """Return checkout shipping price."""
    from .fetch import CheckoutLineInfo

    shipping_method = shipping_method_info.delivery_method

    if lines is not None and all(isinstance(line, CheckoutLineInfo) for line in lines):
        from .utils import is_shipping_required

        shipping_required = is_shipping_required(lines)
    else:
        shipping_required = checkout_info.checkout.is_shipping_required()

    if not shipping_method or not shipping_required:
        return zero_money(checkout_info.checkout.currency)

    return quantize_price(
        shipping_method.price,
        checkout_info.checkout.currency,
    )


def base_checkout_total(
    checkout_info: "CheckoutInfo",
    lines: Iterable["CheckoutLineInfo"],
) -> Money:
    """Return the total cost of the checkout.

    The price includes sales, shipping, specific product and applied once per order
    voucher discounts.
    The price does not include the entire order discount.
    """
    currency = checkout_info.checkout.currency
    subtotal = base_checkout_subtotal(lines, checkout_info.channel, currency)
    shipping_price = base_checkout_delivery_price(checkout_info, lines)

    return subtotal + shipping_price


def base_checkout_subtotal(
    checkout_lines: Iterable["CheckoutLineInfo"],
    channel: "Channel",
    currency: str,
) -> Money:
    """Return the checkout subtotal value.

    The price includes sales, specific product and applied once per order
    voucher discounts.
    The price does not include the entire order discount.
    """
    line_totals = [
        calculate_base_line_total_price(
            line,
            channel,
        )
        for line in checkout_lines
    ]

    return sum(line_totals, zero_money(currency))


def checkout_total(
    checkout_info: "CheckoutInfo",
    lines: Iterable["CheckoutLineInfo"],
) -> Money:
    """Return the total cost of the checkout including discounts and vouchers.

    It should be used as a based value when no flat rate/tax plugin/tax app is active.
    """
    currency = checkout_info.checkout.currency
    subtotal = base_checkout_subtotal(lines, checkout_info.channel, currency)
    shipping_price = base_checkout_delivery_price(checkout_info, lines)
    discount = checkout_info.checkout.discount

    # only entire_order discount with apply_once_per_order set to False is not
    # already included in the total price
    discount_not_included = (
        checkout_info.voucher.type == VoucherType.ENTIRE_ORDER
        and not checkout_info.voucher.apply_once_per_order
        if checkout_info.voucher
        else False
    )
    # Discount is subtracted from both gross and net values, which may cause negative
    # net value if we are having a discount that covers whole price.
    if discount_not_included:
        subtotal = max(zero_money(currency), subtotal - discount)
    return subtotal + shipping_price


def apply_checkout_discount_on_checkout_line(
    checkout_info: "CheckoutInfo",
    lines: Iterable["CheckoutLineInfo"],
    checkout_line_info: "CheckoutLineInfo",
    line_total_price: Money,
):
    """Calculate the checkout line price with discounts.

    Include the entire order voucher discount.
    The discount amount is calculated for every line proportionally to
    the rate of total line price to checkout total price.
    """
    voucher = checkout_info.voucher
    if (
        not voucher
        or voucher.apply_once_per_order
        or voucher.type in [VoucherType.SHIPPING, VoucherType.SPECIFIC_PRODUCT]
    ):
        return line_total_price

    total_discount_amount = checkout_info.checkout.discount_amount
    line_total_price = line_total_price
    currency = checkout_info.checkout.currency

    lines = list(lines)

    # if the checkout has a single line, the whole discount amount will be applied
    # to this line
    if len(lines) == 1:
        return max(
            (line_total_price - Money(total_discount_amount, currency)),
            zero_money(currency),
        )

    # if the checkout has more lines we need to propagate the discount amount
    # proportionally to total prices of items
    lines_total_prices = [
        calculate_base_line_total_price(
            line_info,
            checkout_info.channel,
        ).amount
        for line_info in lines
        if line_info.line.id != checkout_line_info.line.id
    ]

    total_price = sum(lines_total_prices) + line_total_price.amount

    last_element = lines[-1].line.id == checkout_line_info.line.id
    if last_element:
        discount_amount = _calculate_discount_for_last_element(
            lines_total_prices, total_price, total_discount_amount
        )
    else:
        discount_amount = line_total_price.amount / total_price * total_discount_amount
    return max(
        (line_total_price - Money(discount_amount, currency)),
        zero_money(currency),
    )


def _calculate_discount_for_last_element(
    lines_total_prices, total_price, total_discount_amount
):
    """Calculate the discount for last element.

    If the given line is last on the list we should calculate the discount by difference
    between total discount amount and sum of discounts applied to rest of the lines,
    otherwise the sum of discounts won't be equal to the discount amount.
    """
    sum_of_discounts_other_elements = sum(
        [
            line_total_price / total_price * total_discount_amount
            for line_total_price in lines_total_prices
        ]
    )
    return total_discount_amount - sum_of_discounts_other_elements
