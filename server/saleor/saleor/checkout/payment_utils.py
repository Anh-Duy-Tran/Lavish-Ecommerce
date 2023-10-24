"""Checkout-related utility functions."""
from typing import TYPE_CHECKING, Iterable, Optional, Tuple

from prices import Money

from ..core.taxes import zero_money
from . import CheckoutAuthorizeStatus, CheckoutChargeStatus
from .models import Checkout

if TYPE_CHECKING:
    from ..payment.models import TransactionItem


def _update_charge_status(
    checkout: Checkout, checkout_total_gross: Money, total_charged: Money
):
    zero_money_amount = zero_money(checkout.currency)
    total_charged = max(zero_money_amount, total_charged)

    if total_charged <= zero_money_amount and checkout_total_gross != zero_money_amount:
        checkout.charge_status = CheckoutChargeStatus.NONE
    elif total_charged < checkout_total_gross:
        checkout.charge_status = CheckoutChargeStatus.PARTIAL
    elif total_charged == checkout_total_gross:
        checkout.charge_status = CheckoutChargeStatus.FULL
    elif total_charged > checkout_total_gross:
        checkout.charge_status = CheckoutChargeStatus.OVERCHARGED
    else:
        checkout.charge_status = CheckoutChargeStatus.NONE


def _update_authorize_status(
    checkout: Checkout,
    checkout_total_gross: Money,
    total_authorized: Money,
    total_charged: Money,
):
    total_covered = total_authorized + total_charged
    zero_money_amount = zero_money(checkout.currency)
    if total_covered == zero_money_amount and checkout_total_gross != zero_money_amount:
        checkout.authorize_status = CheckoutAuthorizeStatus.NONE
    elif total_covered >= checkout_total_gross:
        checkout.authorize_status = CheckoutAuthorizeStatus.FULL
    elif total_covered < checkout_total_gross and total_covered > zero_money_amount:
        checkout.authorize_status = CheckoutAuthorizeStatus.PARTIAL
    else:
        checkout.authorize_status = CheckoutAuthorizeStatus.NONE


def _get_payment_amount_for_checkout(
    checkout_transactions: Iterable["TransactionItem"], currency: str
) -> Tuple[Money, Money]:
    total_charged_amount = zero_money(currency)
    total_authorized_amount = zero_money(currency)
    for transaction in checkout_transactions:
        total_authorized_amount += transaction.amount_authorized
        total_authorized_amount += transaction.amount_authorize_pending

        total_charged_amount += transaction.amount_charged
        total_charged_amount += transaction.amount_charge_pending
    return total_authorized_amount, total_charged_amount


def update_checkout_payment_statuses(
    checkout: Checkout,
    checkout_total_gross: Money,
    checkout_transactions: Optional[Iterable["TransactionItem"]] = None,
    save: bool = True,
):
    if checkout_transactions is None:
        checkout_transactions = checkout.payment_transactions.all()
    total_authorized_amount, total_charged_amount = _get_payment_amount_for_checkout(
        checkout_transactions, checkout.currency
    )
    _update_authorize_status(
        checkout, checkout_total_gross, total_authorized_amount, total_charged_amount
    )
    _update_charge_status(checkout, checkout_total_gross, total_charged_amount)
    if save:
        checkout.save(
            update_fields=["authorize_status", "charge_status", "last_change"]
        )
