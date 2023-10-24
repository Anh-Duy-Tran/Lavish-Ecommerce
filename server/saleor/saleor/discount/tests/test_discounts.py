from datetime import timedelta
from decimal import Decimal

import graphene
import pytest
from django.utils import timezone
from prices import Money, TaxedMoney

from ...discount.interface import VariantPromotionRuleInfo
from .. import DiscountValueType, RewardValueType, VoucherType
from ..models import NotApplicable, Voucher, VoucherChannelListing, VoucherCustomer
from ..utils import (
    add_voucher_usage_by_customer,
    decrease_voucher_usage,
    get_discount_name,
    get_discount_translated_name,
    increase_voucher_usage,
    remove_voucher_usage_by_customer,
    validate_voucher,
)


def test_valid_voucher_min_spent_amount(channel_USD):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.SHIPPING,
        discount_value_type=DiscountValueType.FIXED,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(10, "USD"),
        min_spent=Money(7, "USD"),
    )
    value = Money(7, "USD")

    voucher.validate_min_spent(value, channel_USD)


def test_valid_voucher_min_spent_amount_not_reached(channel_USD):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.SHIPPING,
        discount_value_type=DiscountValueType.FIXED,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(10, "USD"),
        min_spent=Money(7, "USD"),
    )
    value = Money(5, "USD")

    with pytest.raises(NotApplicable):
        voucher.validate_min_spent(value, channel_USD)


def test_valid_voucher_min_spent_amount_voucher_not_assigned_to_channel(
    channel_USD, channel_PLN
):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.SHIPPING,
        discount_value_type=DiscountValueType.FIXED,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(10, channel_USD.currency_code),
        min_spent=(Money(5, channel_USD.currency_code)),
    )
    price = Money(10, channel_PLN.currency_code)
    total_price = TaxedMoney(net=price, gross=price)
    with pytest.raises(NotApplicable):
        voucher.validate_min_spent(total_price, channel_PLN)


def test_valid_voucher_min_checkout_items_quantity(voucher):
    voucher.min_checkout_items_quantity = 3
    voucher.save()

    with pytest.raises(NotApplicable) as e:
        voucher.validate_min_checkout_items_quantity(2)

    assert (
        str(e.value)
        == "This offer is only valid for orders with a minimum of 3 quantity."
    )


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_percentage_discounts(product, channel_USD, promotion_without_rules):
    # given
    variant = product.variants.get()
    reward_value = Decimal("50")
    rule = promotion_without_rules.rules.create(
        catalogue_predicate={
            "productPredicate": {
                "ids": [graphene.Node.to_global_id("Product", variant.product.id)]
            }
        },
        reward_value_type=RewardValueType.PERCENTAGE,
        reward_value=reward_value,
    )

    variant_channel_listing = variant.channel_listings.get(channel=channel_USD)
    variant_channel_listing.variantlistingpromotionrule.create(
        promotion_rule=rule,
        discount_amount=Decimal("5"),
        currency=channel_USD.currency_code,
    )
    price = Decimal("10")

    # when
    final_price = variant.get_price(
        variant_channel_listing, price, promotion_rules=[rule]
    )

    # then
    assert final_price.amount == price - reward_value / 100 * price


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_fixed_discounts(product, channel_USD, promotion_without_rules):
    # given
    variant = product.variants.get()
    reward_value = Decimal("5")
    rule = promotion_without_rules.rules.create(
        catalogue_predicate={
            "productPredicate": {
                "ids": [graphene.Node.to_global_id("Product", variant.product.id)]
            }
        },
        reward_value_type=RewardValueType.FIXED,
        reward_value=reward_value,
    )

    variant_channel_listing = variant.channel_listings.get(channel=channel_USD)
    variant_channel_listing.variantlistingpromotionrule.create(
        promotion_rule=rule,
        discount_amount=Decimal("1"),
        currency=channel_USD.currency_code,
    )
    price = Decimal("10")

    # when
    final_price = variant.get_price(
        variant_channel_listing, price, promotion_rules=[rule]
    )

    # then
    assert final_price.amount == price - reward_value


def test_voucher_queryset_active(voucher, channel_USD):
    vouchers = Voucher.objects.all()
    assert vouchers.count() == 1
    active_vouchers = Voucher.objects.active_in_channel(
        date=timezone.now() - timedelta(days=1), channel_slug=channel_USD.slug
    )
    assert active_vouchers.count() == 0


def test_voucher_queryset_active_in_channel(voucher, channel_USD):
    vouchers = Voucher.objects.all()
    assert vouchers.count() == 1
    active_vouchers = Voucher.objects.active_in_channel(
        date=timezone.now(), channel_slug=channel_USD.slug
    )
    assert active_vouchers.count() == 1


def test_voucher_queryset_active_in_other_channel(voucher, channel_PLN):
    vouchers = Voucher.objects.all()
    assert vouchers.count() == 1
    active_vouchers = Voucher.objects.active_in_channel(
        date=timezone.now(), channel_slug=channel_PLN.slug
    )
    assert active_vouchers.count() == 0


def test_increase_voucher_usage(channel_USD):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=DiscountValueType.FIXED,
        usage_limit=100,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(10, channel_USD.currency_code),
    )
    increase_voucher_usage(voucher)
    voucher.refresh_from_db()
    assert voucher.used == 1


def test_decrease_voucher_usage(channel_USD):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=DiscountValueType.FIXED,
        usage_limit=100,
        used=10,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(10, channel_USD.currency_code),
    )
    decrease_voucher_usage(voucher)
    voucher.refresh_from_db()
    assert voucher.used == 9


def test_add_voucher_usage_by_customer(voucher, customer_user):
    voucher_customer_count = VoucherCustomer.objects.all().count()
    add_voucher_usage_by_customer(voucher, customer_user.email)
    assert VoucherCustomer.objects.all().count() == voucher_customer_count + 1
    voucherCustomer = VoucherCustomer.objects.first()
    assert voucherCustomer.voucher == voucher
    assert voucherCustomer.customer_email == customer_user.email


def test_add_voucher_usage_by_customer_raise_not_applicable(voucher_customer):
    voucher = voucher_customer.voucher
    customer_email = voucher_customer.customer_email
    with pytest.raises(NotApplicable):
        add_voucher_usage_by_customer(voucher, customer_email)


def test_remove_voucher_usage_by_customer(voucher_customer):
    voucher_customer_count = VoucherCustomer.objects.all().count()
    voucher = voucher_customer.voucher
    customer_email = voucher_customer.customer_email
    remove_voucher_usage_by_customer(voucher, customer_email)
    assert VoucherCustomer.objects.all().count() == voucher_customer_count - 1


def test_remove_voucher_usage_by_customer_not_exists(voucher):
    remove_voucher_usage_by_customer(voucher, "fake@exmaimpel.com")


@pytest.mark.parametrize(
    "total, min_spent_amount, total_quantity, min_checkout_items_quantity,"
    "discount_value_type",
    [
        (20, 20, 2, 2, DiscountValueType.PERCENTAGE),
        (20, None, 2, None, DiscountValueType.PERCENTAGE),
        (20, 20, 2, 2, DiscountValueType.FIXED),
        (20, None, 2, None, DiscountValueType.FIXED),
    ],
)
def test_validate_voucher(
    total,
    min_spent_amount,
    total_quantity,
    min_checkout_items_quantity,
    discount_value_type,
    channel_USD,
):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=discount_value_type,
        min_checkout_items_quantity=min_checkout_items_quantity,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(50, channel_USD.currency_code),
        min_spent_amount=min_spent_amount,
    )
    total_price = Money(total, "USD")
    validate_voucher(
        voucher, total_price, total_quantity, "test@example.com", channel_USD, None
    )


def test_validate_staff_voucher_for_anonymous(
    channel_USD,
):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=DiscountValueType.PERCENTAGE,
        only_for_staff=True,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(50, channel_USD.currency_code),
    )
    total_price = Money(100, "USD")
    price = TaxedMoney(gross=total_price, net=total_price)
    with pytest.raises(NotApplicable):
        validate_voucher(voucher, price, 2, "test@example.com", channel_USD, None)


def test_validate_staff_voucher_for_normal_customer(channel_USD, customer_user):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=DiscountValueType.PERCENTAGE,
        only_for_staff=True,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(50, channel_USD.currency_code),
    )
    total_price = Money(100, "USD")
    price = TaxedMoney(gross=total_price, net=total_price)
    with pytest.raises(NotApplicable):
        validate_voucher(
            voucher, price, 2, customer_user.email, channel_USD, customer_user
        )


def test_validate_staff_voucher_for_staff_customer(channel_USD, staff_user):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=DiscountValueType.PERCENTAGE,
        only_for_staff=True,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(50, channel_USD.currency_code),
    )
    total_price = Money(100, "USD")
    price = TaxedMoney(gross=total_price, net=total_price)

    validate_voucher(voucher, price, 2, staff_user.email, channel_USD, staff_user)


@pytest.mark.parametrize(
    "total, min_spent_amount, total_quantity, min_checkout_items_quantity, "
    "discount_value, discount_value_type",
    [
        (20, 50, 2, 10, 50, DiscountValueType.PERCENTAGE),
        (20, 50, 2, None, 50, DiscountValueType.PERCENTAGE),
        (20, None, 2, 10, 50, DiscountValueType.FIXED),
    ],
)
def test_validate_voucher_not_applicable(
    total,
    min_spent_amount,
    total_quantity,
    min_checkout_items_quantity,
    discount_value,
    discount_value_type,
    channel_USD,
):
    voucher = Voucher.objects.create(
        code="unique",
        type=VoucherType.ENTIRE_ORDER,
        discount_value_type=discount_value_type,
        min_checkout_items_quantity=min_checkout_items_quantity,
    )
    VoucherChannelListing.objects.create(
        voucher=voucher,
        channel=channel_USD,
        discount=Money(50, channel_USD.currency_code),
        min_spent_amount=min_spent_amount,
    )
    total_price = Money(total, "USD")

    with pytest.raises(NotApplicable):
        validate_voucher(
            voucher, total_price, total_quantity, "test@example.com", channel_USD, None
        )


def test_validate_voucher_not_applicable_once_per_customer(
    voucher, customer_user, channel_USD
):
    voucher.apply_once_per_customer = True
    voucher.save()
    VoucherCustomer.objects.create(voucher=voucher, customer_email=customer_user.email)
    price = Money(0, "USD")
    total_price = TaxedMoney(net=price, gross=price)
    with pytest.raises(NotApplicable):
        validate_voucher(
            voucher,
            total_price,
            0,
            customer_user.email,
            channel_USD,
            customer_user,
        )


date_time_now = timezone.now()


def test_get_discount_name_only_rule_name(promotion):
    # given
    promotion.name = ""
    promotion.save(update_fields=["name"])

    rule = promotion.rules.first()

    # when
    name = get_discount_name(rule, promotion)

    # then
    assert name == rule.name


def test_get_discount_name_only_rule_promotion_name(promotion):
    # given
    rule = promotion.rules.first()
    rule.name = ""
    rule.save(update_fields=["name"])

    # when
    name = get_discount_name(rule, promotion)

    # then
    assert name == promotion.name


def test_get_discount_name_rule_and_promotion_name(promotion):
    # given
    rule = promotion.rules.first()

    # when
    name = get_discount_name(rule, promotion)

    # then
    assert name == f"{promotion.name}: {rule.name}"


def test_get_discount_name_empty_names(promotion):
    # given
    rule = promotion.rules.first()

    rule.name = ""
    rule.save(update_fields=["name"])

    promotion.name = ""
    promotion.save(update_fields=["name"])

    # when
    name = get_discount_name(rule, promotion)

    # then
    assert name == ""


def test_get_discount_translated_name_only_rule_translation(rule_info):
    # given
    rule_info_data = rule_info._asdict()
    rule_info_data["promotion_translation"] = None
    rule_info = VariantPromotionRuleInfo(**rule_info_data)

    # when
    translated_name = get_discount_translated_name(rule_info)

    # then
    assert translated_name == rule_info.rule_translation.name


def test_get_discount_translated_name_only_rule_promotion_translation(rule_info):
    # given
    rule_info_data = rule_info._asdict()
    rule_info_data["rule_translation"] = None
    rule_info = VariantPromotionRuleInfo(**rule_info_data)

    # when
    translated_name = get_discount_translated_name(rule_info)

    # then
    assert translated_name == rule_info.promotion_translation.name


def test_get_discount_translated_name_rule_and_promotion_translations(rule_info):
    # when
    translated_name = get_discount_translated_name(rule_info)

    # then
    assert (
        translated_name
        == f"{rule_info.promotion_translation.name}: {rule_info.rule_translation.name}"
    )


def test_get_discount_translated_name_no_translations(rule_info):
    # given
    rule_info_data = rule_info._asdict()
    rule_info_data["promotion_translation"] = None
    rule_info_data["rule_translation"] = None
    rule_info = VariantPromotionRuleInfo(**rule_info_data)

    # when
    translated_name = get_discount_translated_name(rule_info)

    # then
    assert translated_name is None
